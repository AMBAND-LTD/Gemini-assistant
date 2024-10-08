import logging
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import AsyncIterable
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks import AsyncIteratorCallbackHandler
import redis

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load your embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  

class GeminiLLMManager:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.callback = AsyncIteratorCallbackHandler()

        # Load predefined responses
        self.predefined_responses = self.load_predefined_responses()

        # Initialize Redis
        self.redis_client = redis.StrictRedis.from_url(self.redis_url, decode_responses=True)

    def load_predefined_responses(self):
        """Load predefined responses from a JSON file."""
        responses_path = 'predefined_responses.json'  # Path to your predefined responses file
        try:
            with open(responses_path, 'r') as f:
                responses = json.load(f)
                logger.debug(f"Loaded predefined responses: {responses}")
                return responses
        except Exception as e:
            logger.error(f"Error loading predefined responses: {e}")
            return {}

    def get_predefined_response(self, message: str):
        """Fetch predefined response based on the user's message."""
        message_lower = message.lower()
        return self.predefined_responses.get(message_lower)

    def query_redis_data(self, query_vector):
        """Fetch data from Redis based on the user query vector."""
        keys = self.redis_client.keys("embedding:*")  # Fetch all embedding keys
        best_match = None
        best_score = -1

        for key in keys:
            embedding_str = self.redis_client.hget(key, "embedding")
            embedding = np.array(json.loads(embedding_str))
            
            # Calculate cosine similarity
            score = np.dot(embedding, query_vector) / (np.linalg.norm(embedding) * np.linalg.norm(query_vector))
            if score > best_score:
                best_score = score
                best_match = self.redis_client.hget(key, "text")  # Retrieve the associated text

        return best_match

    def create_memory(self):
        """Create memory without session handling."""
        return ConversationBufferWindowMemory(max_token_limit=4000)

    async def add_conversation_to_memory(self, user_message, ai_message):
        # Implement logic to store conversation history if needed
        pass

    def get_gemini_model(self):
        model = ChatGoogleGenerativeAI(
            google_api_key=self.api_key,
            stream=True,
            model="gemini-pro",
            convert_system_message_to_human=True,
            callbacks=[self.callback],
        )
        return model

    async def generate_async_response(self, message: str) -> AsyncIterable[str]:
        model = self.get_gemini_model()
        memory = self.create_memory()
        chat_memory = memory.load_memory_variables({})
        history = chat_memory.get("chat_history", [])

        # Check for predefined response first
        predefined_response = self.get_predefined_response(message)
        if predefined_response:
            yield predefined_response.encode("utf-8", errors="replace")
            return

        # Convert the message into a vector
        query_vector = self.get_vector_from_message(message)

        # Query scraped data from Redis
        scraped_response = self.query_redis_data(query_vector)

        # Prepare message list
        message_list = [SystemMessage(content=os.getenv("SYSTEM_INSTRUCTION", "I am a chatbot."))]
        if history:
            message_list += history

        message_list.append(HumanMessage(content=message))

        # Append the scraped response if available
        if scraped_response:
            message_list.append(HumanMessage(content=self.format_scraped_response(scraped_response)))

        response = ""

        async for token in model.astream(input=message_list):
            response += f"{repr(token.content)}"
            yield f"{repr(token.content)}".encode("utf-8", errors="replace")

        await self.add_conversation_to_memory(message, response)

    def get_vector_from_message(self, message: str):
        """Convert a message to a vector using a pre-trained model."""
        vector = embedding_model.encode(message).tolist()  # Convert to a list

        # Check if the length of the vector is correct
        if len(vector) != 384:
            logger.error(f"Vector length is {len(vector)}, expected 384.")
            raise ValueError(f"Vector length is {len(vector)}, expected 384.")

        logger.debug(f"Generated vector: {vector} with length: {len(vector)}")
        return vector

    def format_scraped_response(self, response: str) -> str:
        """Format the scraped response into a clean and understandable paragraph."""
        # Remove unwanted formatting characters
        formatted_response = response.replace('\n', ' ').replace('*', '').replace('**', '').strip()

        # Remove bullet points (common ones like '-' or '•')
        formatted_response = formatted_response.replace('- ', '').replace('• ', '')

        # Normalize spaces: condense multiple spaces into one
        formatted_response = ' '.join(formatted_response.split())

        # Ensure the response ends with a period if it doesn't already
        if not formatted_response.endswith('.'):
            formatted_response += '.'

        return formatted_response
