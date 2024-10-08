from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .routers.api_v1 import api_router  # Ensure this is the correct import

app = FastAPI(title="Gemini Vision API", version="0.0.1")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; consider limiting this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Serve static files (like CSS and JavaScript)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html") as f:
        return f.read()

# Include the API router with all endpoints
app.include_router(api_router)
