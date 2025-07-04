# Configuration settings for the application
# Module: Configuration
# Created: 2025-07-04

import os
from typing import Dict, Any

class Settings:
    """Application settings"""
    
    def __init__(self):
        # Database settings
        self.database_url = os.getenv("DATABASE_URL", "postgresql://localhost/marketing_funnel")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # ML model settings
        self.ml_model_path = os.getenv("ML_MODEL_PATH", "/tmp/models")
        self.model_cache_ttl = int(os.getenv("MODEL_CACHE_TTL", "3600"))
        
        # Personalization settings
        self.personalization_confidence_threshold = float(os.getenv("PERSONALIZATION_CONFIDENCE_THRESHOLD", "0.7"))
        self.optimization_interval = int(os.getenv("OPTIMIZATION_INTERVAL", "60"))
        
        # Performance settings
        self.max_concurrent_optimizations = int(os.getenv("MAX_CONCURRENT_OPTIMIZATIONS", "100"))
        self.cache_ttl = int(os.getenv("CACHE_TTL", "1800"))
        
        # Logging settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Global settings instance
settings = Settings()