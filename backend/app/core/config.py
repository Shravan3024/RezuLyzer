import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "ResuLyzer"
    TAGLINE: str = "Understand Your Resume. Improve Your Opportunities."
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/resumeiq.db"

    # Security

    SECRET_KEY: str = "resumeiq-super-secret-jwt-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    GUEST_SESSION_EXPIRE_HOURS: int = 24

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # File Storage
    STORAGE_DIR: Path = BASE_DIR / "storage"
    RESUMES_DIR: Path = BASE_DIR / "storage" / "resumes"
    REPORTS_DIR: Path = BASE_DIR / "storage" / "reports"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx"]

    # ATS Scoring Weights (Configurable)
    WEIGHT_REQUIRED_SKILLS: float = 0.35
    WEIGHT_SEMANTIC_SIMILARITY: float = 0.25
    WEIGHT_KEYWORD_RELEVANCE: float = 0.15
    WEIGHT_EXPERIENCE_RELEVANCE: float = 0.10
    WEIGHT_EDUCATION_RELEVANCE: float = 0.10
    WEIGHT_RESUME_STRUCTURE: float = 0.05

    # NLP Model Settings
    ENABLE_TRANSFORMERS: bool = False
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    DEVICE: str = "cpu"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure storage directories exist
os.makedirs(settings.RESUMES_DIR, exist_ok=True)
os.makedirs(settings.REPORTS_DIR, exist_ok=True)
