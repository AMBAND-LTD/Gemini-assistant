# **Installation**

## **1. Install Redis**

- **For Windows:**  
  Download Redis from the following link:  
  [Redis Download](https://github.com/microsoftarchive/redis/releases)

- **Test Redis Installation:**  
  Open a command prompt or PowerShell and run:  
  ```bash
  redis-cli ping
  ```
  You should see a PONG response if Redis is running successfully.

## **2. Clone the Repository**  
Open a command prompt or PowerShell and run:  
```bash
git clone https://github.com/KIMUTAICHELANGA/Gemini-assistant.git
cd Gemini-assistant
```

## **3. Set Up a Virtual Environment**

- **For Linux/macOS:**  
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **For Windows:**  
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

## **4. Install Python Dependencies**  
Use Poetry to install the required dependencies. Ensure that Poetry is installed. If not, you can install it by following the instructions on the [Poetry installation page](https://python-poetry.org/docs/#installation).

Once Poetry is installed, run:  
```bash
poetry install
```

## **5. Configuration**  
Create a `.env` file in the project directory:  
```bash
touch .env
```
Add the following configuration to the `.env` file:  
```plaintext
GEMINI_API_KEY=<your_google_gemini_api_key> # e.g. "1234567890"
REDIS_URL=redis://localhost:6379/0 # Default Redis URL
MY_API_KEY=<your_api_key_to_access_your_backend_api> # e.g. "1234567890"
SYSTEM_INSTRUCTION=<your_system_instruction_for_gemini> # e.g. "give instructions on how to navigate the application...etc"
```

## **6. Running the API**  
Start the FastAPI server:  
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

## **7. API Endpoints**  
- `/conversations/`: Endpoint to handle conversation queries.

## **8. API Documentation**  
Access the Swagger UI for API documentation at:  
`http://localhost:8000/docs`
