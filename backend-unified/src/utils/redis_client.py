# Redis client utilities
# Module: Redis Client
# Created: 2025-07-04

import asyncio
import json
import logging
from typing import Optional, Any
from unittest.mock import AsyncMock

logger = logging.getLogger(__name__)

class MockRedisClient:
    """Mock Redis client for development/testing"""
    
    def __init__(self):
        self.data = {}
        self.expiry = {}
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key"""
        if key in self.expiry:
            import time
            if time.time() > self.expiry[key]:
                del self.data[key]
                del self.expiry[key]
                return None
        return self.data.get(key)
    
    async def set(self, key: str, value: str) -> bool:
        """Set key-value pair"""
        self.data[key] = value
        return True
    
    async def setex(self, key: str, ttl: int, value: str) -> bool:
        """Set key-value pair with expiry"""
        import time
        self.data[key] = value
        self.expiry[key] = time.time() + ttl
        return True
    
    async def delete(self, key: str) -> int:
        """Delete key"""
        if key in self.data:
            del self.data[key]
            if key in self.expiry:
                del self.expiry[key]
            return 1
        return 0
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return key in self.data

# Global mock Redis client instance
_redis_client = MockRedisClient()

def get_redis_client():
    """Get Redis client instance"""
    return _redis_client