Gemini Assistant
Gemini Assistant is a virtual assistant/chatbot that helps with navigation within the APHRC. It integrates multiple AI models to provide advanced conversational flows, leveraging Google's Gemini APIs for enhanced comprehension and generation.

Features
Langchain Integration: Utilizes multiple AI models to enable advanced conversational flows.
Google Gemini API: Integrates Gemini, Gemini Pro, and Gemini Pro Vision for improved conversational comprehension and generation capabilities.
Ephemeral Conversation Storage: Uses Redis for efficient memory management and ensures data privacy.
User-Friendly Interface: Streamlined API endpoints for easy integration and smooth navigation.
Getting Started
Prerequisites
Google Gemini API:

Obtain a Google Gemini AI API key from Google Gemini AI.
Add the key to your project’s Secrets or environment variables with the key GOOGLE_API_KEY.
Langchain-Gemini-API Requirements:

Python 3.9 or higher
FastAPI
Uvicorn
Redis
Access to the Google Gemini API
Installation
1. Install Redis
For Linux:

bash
Copy code
sudo apt update
sudo apt install redis-server
For Windows: Download Redis from here.

Test Redis Installation:

bash
Copy code
redis-cli ping
You should see a PONG response if Redis is running successfully.

2. Clone the Repository
bash
Copy code
git clone https://github.com/KIMUTAICHELANGA/Gemini-assistant.git
cd Gemini-assistant
3. Set Up a Virtual Environment
For Linux/macOS:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
For Windows:

bash
Copy code
python -m venv venv
venv\Scripts\activate
4. Install Python Dependencies
bash
Copy code
poetry install
Configuration
Create a .env file in the project directory:

bash
Copy code
touch .env
Add the following configuration to the .env file:

makefile
Copy code
GEMINI_API_KEY=<your_google_gemini_api_key>
REDIS_URL=redis://localhost:6379/0  # Default Redis URL
MY_API_KEY=<your_api_key_to_access_your_backend_api>
SYSTEM_INSTRUCTION=<your_system_instruction_for_gemini>
Running the API
Start the FastAPI server:

bash
Copy code
uvicorn app.main:app --reload
The API will be available at http://localhost:8000.

API Endpoints
/conversations/: Endpoint to handle conversation queries.
API Documentation
Access the Swagger UI for API documentation at:
http://localhost:8000/docs
