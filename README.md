Gemini Assistant
Overview
Gemini Assistant is a virtual assistant/chatbot that helps with navigation within aphrc

Features
Langchain Integration: Enabling advanced conversational flows by utilizing multiple AI models.
Google Gemini API: Integrating Gemini, Gemini Pro, and Gemini Pro Vision for enhanced conversational comprehension and generation.
Ephemeral Conversation Storage: Using Redis for efficient memory management and ensuring data privacy.
User-Friendly Interface: Streamlined API endpoints designed for easy integration.
Getting Started
Prerequisites for Google Gemini API
Get a Google Gemini AI API key here and add it to Secrets in your Repl with the key GOOGLE_API_KEY.
Prerequisites for langchain-gemini-api
Python 3.9 or higher
FastAPI
Uvicorn
Redis
Access to Google Gemini API
Installation
Install Redis
Install Redis:
sudo apt update
sudo apt install redis-server
Windows users can download Redis from here
Test Redis:
redis-cli ping
If Redis is running, it will return PONG.
Install Python Dependencies
Clone the repository:
https://github.com/KIMUTAICHELANGA/Gemini-assistant.git
Create a virtual environment:
python3 -m venv venv
for Windows:
python -m venv venv
Activate the virtual environment:
 source venv/bin/activate

poetry install
Configuration
Create a .env file in the project directory and add the following:
GEMINI_API_KEY=<your_google_gemini_api_key> # e.g. "1234567890"
REDIS_URL=redis://localhost:6379/0 # default Redis URL
MY_API_KEY=<your_api_key_to_access_your_backend_api> . "1234567890"
SYSTEM_INSTRUCTION=<your_system_instruction_for_gemini> # e.g. "give instructions on how to navigate the application...etc"
Running the API
Start fastapi server:
uvicorn app.main:app --reload
The API will be available at http://localhost:8000.

API Endpoints
/conversations/: Endpoint for conversation

API Documentation
/docs: Swagger UI for API documentation.
