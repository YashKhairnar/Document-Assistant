from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Document Assistant"
    DEBUG: bool = False
    
    # Model Settings
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Gemini Settings (if used)
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    # Directory Settings
    STATIC_DIR: str = "app/static"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
