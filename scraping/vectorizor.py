import os
import json  # Add this import statement
import jsonlines  # Import jsonlines to handle JSON Lines format
import torch
import redis
import numpy as np
from transformers import AutoTokenizer, AutoModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load models
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Updated model name
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# Expected output size of the model
EXPECTED_EMBEDDING_SIZE = 384  # Model outputs 384-dimensional embeddings

# Initialize Redis
def initialize_redis():
    redis_host = os.getenv("REDIS_HOST", "localhost").strip()  # Strip whitespace
    redis_port = int(os.getenv("REDIS_PORT", "6379").strip())  # Ensure this is an integer, strip spaces

    # Initialize Redis client without password
    r = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        decode_responses=True
    )
    return r

# Load data from JSONL file
def load_data(file_path):
    data = []
    with jsonlines.open(file_path) as f:
        for item in f:
            if 'text' in item and 'source' in item:
                data.append(item)
    return data

# Create embeddings
def create_embeddings(text_batch):
    inputs = tokenizer(text_batch, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Average pooling
    
    # Convert to list format and check size
    embedding_list = embeddings.numpy().tolist()
    for embedding in embedding_list:
        if len(embedding) != EXPECTED_EMBEDDING_SIZE:
            raise ValueError(f"Embedding size mismatch: expected {EXPECTED_EMBEDDING_SIZE}, got {len(embedding)}.")
    
    return embedding_list  # Return the list of embeddings

# Create and store embeddings in Redis using hashes
def create_and_store_embeddings(data, redis_client):
    for item in data:
        if "text" in item and "source" in item:
            text = item["text"]
            source = item["source"]
            embedding = create_embeddings([text])[0]  # Create embedding for this text
            
            # Store in Redis using hashes
            redis_key = f"embedding:{source.split('/')[-1]}"
            redis_client.hset(redis_key, mapping={
                "embedding": json.dumps(embedding),  # Store the embedding as a JSON string
                "source": source,
                "text": text
            })

# Main function
def main():
    DATA_FILE = os.path.join("data", "vectorizor.jsonl")  # Updated path to JSONL file
    redis_client = initialize_redis()
    
    data = load_data(DATA_FILE)
    create_and_store_embeddings(data, redis_client)

if __name__ == "__main__":
    main()
