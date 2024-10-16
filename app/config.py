from pydantic import BaseSettings

class Settings(BaseSettings):
    MY_API_KEY: str
    GEMINI_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379/5"
    SYSTEM_INSTRUCTION: str = "It should guide the user through the website."
    REDIS_HOST: str
    REDIS_PORT: int

# Example of how to use the Settings class
settings = Settings(
    MY_API_KEY="your_actual_api_key_here",
    GEMINI_API_KEY="AIzaSyDDWipE4AuI8UvWkMYOom6rh9zFytd6Gos",
    REDIS_HOST="localhost",
    REDIS_PORT=6379
)

