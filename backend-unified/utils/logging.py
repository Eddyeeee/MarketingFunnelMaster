#!/usr/bin/env python3
"""
Logging Configuration
Basic logging setup

Executor: Claude Code
Erstellt: 2025-07-03
"""

import logging
import sys
from typing import Optional

def setup_logging(level: Optional[str] = None):
    """Setup basic logging configuration"""
    log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reduce noise from external libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {log_level}")
    
    return logger