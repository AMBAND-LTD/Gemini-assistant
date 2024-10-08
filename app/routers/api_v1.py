from fastapi import APIRouter
from app.api.endpoints.v1 import conversation, conversation_delete

api_router = APIRouter()

# Include the conversation router
api_router.include_router(
    conversation.router,
    prefix="/api/v1/conversations",  # Prefix for conversation endpoints
    tags=["conversation"]  # Tag for documentation
)

# Include the conversation delete router
api_router.include_router(
    conversation_delete.router,
    prefix="/api/v1/delete",  # Prefix for deletion endpoints
    tags=["conversation-delete"]  # Tag for documentation
)

# Example of how you might structure the conversation router
@conversation.router.post("/")
async def create_conversation(conversation_data: dict):
    # Logic to create a conversation
    return {"message": "Conversation created", "data": conversation_data}

# Example of how you might structure the conversation delete router
@conversation_delete.router.delete("/")
async def delete_conversation():
    # Logic to delete the last conversation or all conversations
    # For example, delete the last conversation
    # (You would need to implement the actual deletion logic here)
    return {"message": "Last conversation deleted"}

# Alternatively, if you want to delete all conversations, use:
@conversation_delete.router.delete("/all")
async def delete_all_conversations():
    # Logic to delete all conversations
    # (You would need to implement the actual deletion logic here)
    return {"message": "All conversations deleted"}
