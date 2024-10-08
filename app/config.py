from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MY_API_KEY: str
    GEMINI_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379/5"
    SYSTEM_INSTRUCTION: str = "It should guide the user through the website."
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"
