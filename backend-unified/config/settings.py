#!/usr/bin/env python3
"""
Configuration Settings for MarketingFunnelMaster Unified Backend
Environment-based configuration management

Executor: Claude Code
Erstellt: 2025-07-03
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application Configuration
    APP_NAME: str = "MarketingFunnelMaster"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=True, description="Debug mode")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=4, description="Number of worker processes for production")
    
    # Security Configuration
    SECRET_KEY: str = Field(..., description="Secret key for JWT and encryption")
    JWT_SECRET: str = Field(..., description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRATION_HOURS: int = Field(default=24, description="JWT token expiration in hours")
    API_KEY_PREFIX: str = Field(default="mfm_", description="API key prefix")
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173",
            "https://app.marketingfunnelmaster.com",
            "https://dashboard.marketingfunnelmaster.com"
        ],
        description="Allowed CORS origins"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=[
            "localhost",
            "127.0.0.1",
            "api.marketingfunnelmaster.com",
            "backend.marketingfunnelmaster.com"
        ],
        description="Allowed hosts for production"
    )
    
    # Database Configuration (PostgreSQL via Supabase)
    DATABASE_URL: str = Field(..., description="PostgreSQL database URL")
    DATABASE_POOL_SIZE: int = Field(default=20, description="Database connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=30, description="Database max overflow connections")
    DATABASE_ECHO: bool = Field(default=False, description="Echo SQL queries")
    
    # Migration Database (SQLite - temporary during migration)
    SQLITE_DATABASE_PATH: str = Field(
        default="./data/migration.db",
        description="SQLite database path for migration"
    )
    
    # Redis Configuration (Caching & Sessions)
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    REDIS_POOL_SIZE: int = Field(default=10, description="Redis connection pool size")
    
    # AI & ML Configuration
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    ANTHROPIC_API_KEY: str = Field(..., description="Anthropic Claude API key")
    GOOGLE_AI_API_KEY: Optional[str] = Field(None, description="Google AI API key")
    
    # ChromaDB Configuration (Vector Storage)
    CHROMADB_HOST: str = Field(default="localhost", description="ChromaDB host")
    CHROMADB_PORT: int = Field(default=8000, description="ChromaDB port")
    CHROMADB_COLLECTION_NAME: str = Field(
        default="marketing_intelligence",
        description="ChromaDB collection name"
    )
    
    # External API Configuration
    AWIN_API_KEY: Optional[str] = Field(None, description="AWIN Affiliate API key")
    AWIN_PUBLISHER_ID: Optional[str] = Field(None, description="AWIN Publisher ID")
    DIGISTORE24_API_KEY: Optional[str] = Field(None, description="Digistore24 API key")
    N8N_WEBHOOK_URL: Optional[str] = Field(None, description="N8N webhook URL")
    
    # Email Service Configuration
    SENDGRID_API_KEY: Optional[str] = Field(None, description="SendGrid API key")
    MAILGUN_API_KEY: Optional[str] = Field(None, description="Mailgun API key")
    MAILGUN_DOMAIN: Optional[str] = Field(None, description="Mailgun domain")
    
    # Cloud Infrastructure Configuration
    HETZNER_API_TOKEN: Optional[str] = Field(None, description="Hetzner Cloud API token")
    CLOUDFLARE_API_TOKEN: Optional[str] = Field(None, description="Cloudflare API token")
    CLOUDFLARE_ZONE_ID: Optional[str] = Field(None, description="Cloudflare Zone ID")
    
    # Monitoring & Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    SENTRY_DSN: Optional[str] = Field(None, description="Sentry DSN for error tracking")
    PROMETHEUS_ENABLED: bool = Field(default=False, description="Enable Prometheus metrics")
    
    # Rate Limiting Configuration
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, description="API rate limit per minute")
    RATE_LIMIT_BURST: int = Field(default=200, description="Rate limit burst capacity")
    
    # Agent Configuration
    MAX_CONCURRENT_AGENTS: int = Field(default=50, description="Maximum concurrent agents")
    AGENT_TIMEOUT_SECONDS: int = Field(default=300, description="Agent task timeout in seconds")
    WEBSOCKET_HEARTBEAT_INTERVAL: int = Field(default=30, description="WebSocket heartbeat interval")
    
    # Website Generation Configuration
    MAX_WEBSITES_PER_USER: int = Field(default=1500, description="Maximum websites per user")
    WEBSITE_GENERATION_TIMEOUT: int = Field(default=900, description="Website generation timeout")
    DEFAULT_WEBSITE_TEMPLATE: str = Field(
        default="nextjs-tailwind",
        description="Default website template"
    )
    
    # Performance Configuration
    CACHE_TTL_SECONDS: int = Field(default=300, description="Default cache TTL")
    BACKGROUND_TASK_QUEUE_SIZE: int = Field(default=1000, description="Background task queue size")
    MAX_REQUEST_SIZE: int = Field(default=50 * 1024 * 1024, description="Max request size (50MB)")
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validate environment value"""
        if v not in ["development", "staging", "production"]:
            raise ValueError("Environment must be development, staging, or production")
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == "production"
    
    @property
    def database_config(self) -> dict:
        """Get database configuration dict"""
        return {
            "url": self.DATABASE_URL,
            "pool_size": self.DATABASE_POOL_SIZE,
            "max_overflow": self.DATABASE_MAX_OVERFLOW,
            "echo": self.DATABASE_ECHO and self.is_development
        }
    
    @property
    def redis_config(self) -> dict:
        """Get Redis configuration dict"""
        return {
            "url": self.REDIS_URL,
            "pool_size": self.REDIS_POOL_SIZE
        }
    
    @property
    def ai_config(self) -> dict:
        """Get AI service configuration dict"""
        return {
            "openai_api_key": self.OPENAI_API_KEY,
            "anthropic_api_key": self.ANTHROPIC_API_KEY,
            "google_ai_api_key": self.GOOGLE_AI_API_KEY,
            "chromadb": {
                "host": self.CHROMADB_HOST,
                "port": self.CHROMADB_PORT,
                "collection_name": self.CHROMADB_COLLECTION_NAME
            }
        }
    
    @property
    def external_apis_config(self) -> dict:
        """Get external APIs configuration dict"""
        return {
            "awin": {
                "api_key": self.AWIN_API_KEY,
                "publisher_id": self.AWIN_PUBLISHER_ID
            },
            "digistore24": {
                "api_key": self.DIGISTORE24_API_KEY
            },
            "n8n": {
                "webhook_url": self.N8N_WEBHOOK_URL
            }
        }
    
    @property
    def cloud_config(self) -> dict:
        """Get cloud infrastructure configuration dict"""
        return {
            "hetzner": {
                "api_token": self.HETZNER_API_TOKEN
            },
            "cloudflare": {
                "api_token": self.CLOUDFLARE_API_TOKEN,
                "zone_id": self.CLOUDFLARE_ZONE_ID
            }
        }
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Create data directories if they don't exist
def create_data_directories():
    """Create necessary data directories"""
    directories = [
        Path(settings.SQLITE_DATABASE_PATH).parent,
        Path("./logs"),
        Path("./data/uploads"),
        Path("./data/exports"),
        Path("./data/cache")
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize data directories
create_data_directories()

# Environment-specific configuration adjustments
if settings.is_production:
    # Production optimizations
    settings.DEBUG = False
    settings.DATABASE_ECHO = False
    settings.LOG_LEVEL = "WARNING"
elif settings.ENVIRONMENT == "staging":
    # Staging configuration
    settings.DEBUG = False
    settings.LOG_LEVEL = "INFO"

# Configuration validation
def validate_required_settings():
    """Validate that all required settings are present"""
    required_settings = [
        "SECRET_KEY",
        "JWT_SECRET", 
        "DATABASE_URL",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY"
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_settings)}\n"
            f"Please set these in your .env file or environment variables."
        )

# Validate settings on import
try:
    validate_required_settings()
except ValueError as e:
    if not settings.is_development:
        raise e
    else:
        print(f"⚠️ Configuration warning: {e}")
        print("⚠️ Some features may not work correctly in development mode.")

# Export settings instance
__all__ = ["settings"]