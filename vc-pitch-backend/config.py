"""
Configuration settings for VC Pitch Generator
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # API Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"  # ← CHANGED THIS
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # Rest stays the same...
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",      # serve / React dev
        "http://localhost:5173",      # Vite dev
        "http://localhost:5500",      # VS Code Live Server
        "http://localhost:5501",      # VS Code Live Server alt
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5501",
        "null",                       # local file opening
        "*"
    ]
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    REQUESTS_PER_MINUTE: int = 10
    REQUESTS_PER_HOUR: int = 100
    
    # API Settings
    API_TIMEOUT: int = 30
    MAX_IDEA_LENGTH: int = 200
    MIN_IDEA_LENGTH: int = 10
    
    def __init__(self):
        """Initialize settings"""
        if not self.GROQ_API_KEY:
            raise ValueError(
                "❌ GROQ_API_KEY environment variable not set. "
                "Get one at https://console.groq.com/keys"
            )
        
        # Parse ALLOWED_ORIGINS from env if provided
        origins_env = os.getenv("ALLOWED_ORIGINS", "")
        if origins_env:
            self.ALLOWED_ORIGINS = [
                origin.strip() for origin in origins_env.split(",")
            ]


# Create settings instance
settings = Settings()