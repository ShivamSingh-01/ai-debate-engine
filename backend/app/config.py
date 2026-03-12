from pydantic_settings import BaseSettings
from typing import Optional
class Settings(BaseSettings):
    groq_api_key: str = ""
    tavily_api_key: str = ""
    model_name: str = "llama-3.3-70b-versatile"
    debate_rounds: int = 3
    class Config:
        env_file = ".env"
        extra = "allow"
settings = Settings()