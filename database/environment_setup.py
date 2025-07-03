"""
Environment Setup and Configuration Management
Handles environment variables, secrets, and configuration validation
Version: 1.0.0
Created: 2025-07-03
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import json

logger = logging.getLogger(__name__)

@dataclass
class DatabaseCredentials:
    """Database connection credentials"""
    # Neon PostgreSQL
    neon_host: str
    neon_port: int
    neon_database: str
    neon_user: str
    neon_password: str
    neon_sslmode: str = "require"
    
    # Neo4j
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str = "neo4j"

@dataclass
class ApplicationConfig:
    """Application configuration settings"""
    # Environment
    environment: str = "development"  # development, staging, production
    debug: bool = False
    log_level: str = "INFO"
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1
    
    # Performance Settings
    max_concurrent_requests: int = 100
    request_timeout_seconds: int = 30
    
    # Database Settings
    db_min_connections: int = 5
    db_max_connections: int = 20
    db_command_timeout: int = 60
    
    # Monitoring Settings
    enable_metrics: bool = True
    health_check_interval: int = 30
    metrics_retention_days: int = 7
    
    # Learning System Settings
    learning_rate: float = 0.01
    confidence_threshold: float = 0.7
    performance_measurement_window_days: int = 7

class EnvironmentManager:
    """Manages environment configuration and validation"""
    
    def __init__(self):
        self.config_loaded = False
        self.credentials: Optional[DatabaseCredentials] = None
        self.app_config: Optional[ApplicationConfig] = None
        
    def load_configuration(self) -> bool:
        """Load and validate all configuration"""
        try:
            # Load database credentials
            self.credentials = self._load_database_credentials()
            
            # Load application configuration
            self.app_config = self._load_application_config()
            
            # Validate configuration
            self._validate_configuration()
            
            self.config_loaded = True
            logger.info("Configuration loaded and validated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False
    
    def _load_database_credentials(self) -> DatabaseCredentials:
        """Load database credentials from environment variables"""
        # Required environment variables
        required_vars = [
            "NEON_PASSWORD",
            "NEO4J_PASSWORD"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {missing_vars}")
        
        return DatabaseCredentials(
            # Neon PostgreSQL
            neon_host=os.getenv("NEON_HOST", "ep-xxx-xxx.us-east-1.aws.neon.tech"),
            neon_port=int(os.getenv("NEON_PORT", "5432")),
            neon_database=os.getenv("NEON_DATABASE", "marketing_funnel_rag"),
            neon_user=os.getenv("NEON_USER", "neon_user"),
            neon_password=os.getenv("NEON_PASSWORD"),
            neon_sslmode=os.getenv("NEON_SSLMODE", "require"),
            
            # Neo4j
            neo4j_uri=os.getenv("NEO4J_URI", "neo4j+s://your-instance.databases.neo4j.io"),
            neo4j_username=os.getenv("NEO4J_USERNAME", "neo4j"),
            neo4j_password=os.getenv("NEO4J_PASSWORD"),
            neo4j_database=os.getenv("NEO4J_DATABASE", "neo4j")
        )
    
    def _load_application_config(self) -> ApplicationConfig:
        """Load application configuration from environment variables"""
        return ApplicationConfig(
            # Environment
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            
            # API Settings
            api_host=os.getenv("API_HOST", "0.0.0.0"),
            api_port=int(os.getenv("API_PORT", "8000")),
            api_workers=int(os.getenv("API_WORKERS", "1")),
            
            # Performance Settings
            max_concurrent_requests=int(os.getenv("MAX_CONCURRENT_REQUESTS", "100")),
            request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30")),
            
            # Database Settings
            db_min_connections=int(os.getenv("DB_MIN_CONNECTIONS", "5")),
            db_max_connections=int(os.getenv("DB_MAX_CONNECTIONS", "20")),
            db_command_timeout=int(os.getenv("DB_COMMAND_TIMEOUT", "60")),
            
            # Monitoring Settings
            enable_metrics=os.getenv("ENABLE_METRICS", "true").lower() == "true",
            health_check_interval=int(os.getenv("HEALTH_CHECK_INTERVAL", "30")),
            metrics_retention_days=int(os.getenv("METRICS_RETENTION_DAYS", "7")),
            
            # Learning System Settings
            learning_rate=float(os.getenv("LEARNING_RATE", "0.01")),
            confidence_threshold=float(os.getenv("CONFIDENCE_THRESHOLD", "0.7")),
            performance_measurement_window_days=int(os.getenv("PERFORMANCE_MEASUREMENT_WINDOW_DAYS", "7"))
        )
    
    def _validate_configuration(self) -> None:
        """Validate loaded configuration"""
        if not self.credentials or not self.app_config:
            raise ValueError("Configuration not loaded")
        
        # Validate database credentials
        if not self.credentials.neon_password:
            raise ValueError("Neon password is required")
        
        if not self.credentials.neo4j_password:
            raise ValueError("Neo4j password is required")
        
        # Validate application config
        if self.app_config.db_min_connections >= self.app_config.db_max_connections:
            raise ValueError("db_min_connections must be less than db_max_connections")
        
        if self.app_config.learning_rate <= 0 or self.app_config.learning_rate >= 1:
            raise ValueError("learning_rate must be between 0 and 1")
        
        if self.app_config.confidence_threshold <= 0 or self.app_config.confidence_threshold >= 1:
            raise ValueError("confidence_threshold must be between 0 and 1")
    
    def get_database_url(self, database: str = "postgresql") -> str:
        """Get database connection URL"""
        if not self.config_loaded:
            raise RuntimeError("Configuration not loaded")
        
        if database == "postgresql":
            return (
                f"postgresql://{self.credentials.neon_user}:{self.credentials.neon_password}"
                f"@{self.credentials.neon_host}:{self.credentials.neon_port}"
                f"/{self.credentials.neon_database}?sslmode={self.credentials.neon_sslmode}"
            )
        elif database == "neo4j":
            return self.credentials.neo4j_uri
        else:
            raise ValueError(f"Unknown database: {database}")
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get environment information for debugging"""
        if not self.config_loaded:
            return {"error": "Configuration not loaded"}
        
        return {
            "environment": self.app_config.environment,
            "debug": self.app_config.debug,
            "log_level": self.app_config.log_level,
            "api_host": self.app_config.api_host,
            "api_port": self.app_config.api_port,
            "database_configured": bool(self.credentials),
            "neon_host": self.credentials.neon_host if self.credentials else None,
            "neo4j_configured": bool(self.credentials and self.credentials.neo4j_uri),
            "monitoring_enabled": self.app_config.enable_metrics,
            "health_check_interval": self.app_config.health_check_interval
        }
    
    def create_env_template(self, file_path: str = ".env.template") -> None:
        """Create environment template file"""
        template_content = """# Agentic RAG System Environment Configuration
# Copy this file to .env and fill in your actual values

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# Neon PostgreSQL Database
NEON_HOST=ep-xxx-xxx.us-east-1.aws.neon.tech
NEON_PORT=5432
NEON_DATABASE=marketing_funnel_rag
NEON_USER=neon_user
NEON_PASSWORD=your_neon_password_here
NEON_SSLMODE=require

# Neo4j Database
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password_here
NEO4J_DATABASE=neo4j

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1

# Performance Settings
MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT_SECONDS=30

# Database Connection Pool
DB_MIN_CONNECTIONS=5
DB_MAX_CONNECTIONS=20
DB_COMMAND_TIMEOUT=60

# ============================================================================
# MONITORING AND PERFORMANCE
# ============================================================================

# Monitoring
ENABLE_METRICS=true
HEALTH_CHECK_INTERVAL=30
METRICS_RETENTION_DAYS=7
ENABLE_QUERY_LOGGING=true
SLOW_QUERY_THRESHOLD_MS=1000
SLOW_GRAPH_QUERY_THRESHOLD_MS=2000

# ============================================================================
# AI AND LEARNING SYSTEM
# ============================================================================

# Learning System
LEARNING_RATE=0.01
CONFIDENCE_THRESHOLD=0.7
PERFORMANCE_MEASUREMENT_WINDOW_DAYS=7

# Vector Search
PGVECTOR_HNSW_M=16
PGVECTOR_HNSW_EF_CONSTRUCTION=64
PGVECTOR_HNSW_EF_SEARCH=32

# ============================================================================
# SECURITY AND OPTIMIZATION
# ============================================================================

# Graph Configuration
GRAPHITI_TEMPORAL_RESOLUTION=day
GRAPHITI_CONFIDENCE_THRESHOLD=0.7
GRAPHITI_MAX_ENTITIES_PER_EXTRACTION=50

# Performance Optimization
GRAPH_MAX_SEARCH_DEPTH=3
GRAPH_MIN_CONFIDENCE_SCORE=0.6
GRAPH_CONNECTION_POOL_SIZE=50

# Sync Configuration
SYNC_FREQUENCY_SECONDS=300
SYNC_BATCH_SIZE=100
CONFLICT_RESOLUTION_STRATEGY=latest_wins

# ============================================================================
# OPTIONAL INTEGRATIONS
# ============================================================================

# OpenAI (for embeddings)
# OPENAI_API_KEY=your_openai_api_key_here

# Other AI Services
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# GOOGLE_API_KEY=your_google_api_key_here

# ============================================================================
# DEPLOYMENT SETTINGS
# ============================================================================

# Production deployment settings (uncomment for production)
# ENVIRONMENT=production
# DEBUG=false
# LOG_LEVEL=WARNING
# API_WORKERS=4
# DB_MAX_CONNECTIONS=50
# HEALTH_CHECK_INTERVAL=60
"""
        
        with open(file_path, 'w') as f:
            f.write(template_content)
        
        logger.info(f"Environment template created at {file_path}")
    
    def validate_production_readiness(self) -> Dict[str, Any]:
        """Validate configuration for production deployment"""
        if not self.config_loaded:
            return {"ready": False, "error": "Configuration not loaded"}
        
        issues = []
        warnings = []
        
        # Check environment
        if self.app_config.environment != "production":
            warnings.append("Environment is not set to 'production'")
        
        if self.app_config.debug:
            issues.append("Debug mode should be disabled in production")
        
        # Check database configuration
        if "localhost" in self.credentials.neon_host or "127.0.0.1" in self.credentials.neon_host:
            issues.append("Using localhost database in production")
        
        if "localhost" in self.credentials.neo4j_uri or "127.0.0.1" in self.credentials.neo4j_uri:
            issues.append("Using localhost Neo4j in production")
        
        # Check security
        if len(self.credentials.neon_password) < 12:
            issues.append("Neon password should be at least 12 characters")
        
        if len(self.credentials.neo4j_password) < 12:
            issues.append("Neo4j password should be at least 12 characters")
        
        # Check performance settings
        if self.app_config.db_max_connections < 20:
            warnings.append("Consider increasing max database connections for production")
        
        if self.app_config.api_workers < 2:
            warnings.append("Consider using multiple API workers for production")
        
        # Check monitoring
        if not self.app_config.enable_metrics:
            issues.append("Metrics should be enabled in production")
        
        production_ready = len(issues) == 0
        
        return {
            "ready": production_ready,
            "issues": issues,
            "warnings": warnings,
            "total_issues": len(issues),
            "total_warnings": len(warnings)
        }
    
    def export_config_summary(self, file_path: str = "config_summary.json") -> None:
        """Export configuration summary for documentation"""
        if not self.config_loaded:
            raise RuntimeError("Configuration not loaded")
        
        summary = {
            "environment": self.app_config.environment,
            "database_configuration": {
                "postgresql": {
                    "host": self.credentials.neon_host,
                    "port": self.credentials.neon_port,
                    "database": self.credentials.neon_database,
                    "user": self.credentials.neon_user,
                    "ssl_mode": self.credentials.neon_sslmode
                },
                "neo4j": {
                    "uri": self.credentials.neo4j_uri,
                    "username": self.credentials.neo4j_username,
                    "database": self.credentials.neo4j_database
                }
            },
            "application_settings": {
                "api_host": self.app_config.api_host,
                "api_port": self.app_config.api_port,
                "debug": self.app_config.debug,
                "max_concurrent_requests": self.app_config.max_concurrent_requests,
                "database_connection_pool": {
                    "min_connections": self.app_config.db_min_connections,
                    "max_connections": self.app_config.db_max_connections,
                    "command_timeout": self.app_config.db_command_timeout
                }
            },
            "monitoring": {
                "enabled": self.app_config.enable_metrics,
                "health_check_interval": self.app_config.health_check_interval,
                "metrics_retention_days": self.app_config.metrics_retention_days
            },
            "learning_system": {
                "learning_rate": self.app_config.learning_rate,
                "confidence_threshold": self.app_config.confidence_threshold,
                "measurement_window_days": self.app_config.performance_measurement_window_days
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Configuration summary exported to {file_path}")

# Global environment manager
env_manager = EnvironmentManager()

# Helper functions
def load_environment() -> bool:
    """Load environment configuration"""
    return env_manager.load_configuration()

def get_database_credentials() -> DatabaseCredentials:
    """Get database credentials"""
    if not env_manager.config_loaded:
        raise RuntimeError("Environment not loaded")
    return env_manager.credentials

def get_app_config() -> ApplicationConfig:
    """Get application configuration"""
    if not env_manager.config_loaded:
        raise RuntimeError("Environment not loaded")
    return env_manager.app_config

def validate_environment() -> bool:
    """Validate environment configuration"""
    try:
        env_manager._validate_configuration()
        return True
    except Exception as e:
        logger.error(f"Environment validation failed: {e}")
        return False

if __name__ == "__main__":
    # Test environment setup
    try:
        # Create environment template
        env_manager.create_env_template(".env.example")
        print("Environment template created")
        
        # Try to load configuration (will fail without real values)
        try:
            success = load_environment()
            if success:
                print("Configuration loaded successfully")
                
                # Get environment info
                info = env_manager.get_environment_info()
                print(f"Environment: {info['environment']}")
                
                # Check production readiness
                readiness = env_manager.validate_production_readiness()
                print(f"Production ready: {readiness['ready']}")
                
            else:
                print("Configuration loading failed (expected without real credentials)")
                
        except Exception as e:
            print(f"Configuration loading failed: {e} (expected without real credentials)")
        
    except Exception as e:
        print(f"Environment setup test failed: {e}")