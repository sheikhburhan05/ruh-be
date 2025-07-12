from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Wellness Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    DATABASE_USER: str = os.getenv("DATABASE_USER", "")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "")
    DATABASE_PORT: int = os.getenv("DATABASE_PORT", 16348)
    DATABASE_SSLMODE: str = os.getenv("DATABASE_SSLMODE", "")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API Sync Settings
    SYNC_INTERVAL_MINUTES: int = 5

    class Config:
        case_sensitive = True

settings = Settings() 