from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import ChatRequest
from app.utils.message_handler import MessageHandler
from app.utils.llm_manager import GeminiLLMManager

router = APIRouter()

llm_manager = GeminiLLMManager()
message_handler = MessageHandler(llm_manager)

@router.post("/")
async def chat_with_model(chat_request: ChatRequest):
    try:
        message = chat_request.query  # Only using the query from the ChatRequest schema
        # Adjust the method call if it does not require a conversation ID
        return StreamingResponse(message_handler.send_message_async(message),
                                 media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
