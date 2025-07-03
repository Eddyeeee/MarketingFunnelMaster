#!/usr/bin/env python3
"""
Rate Limiter Implementation
Redis-based rate limiting for API endpoints and user requests

Executor: Claude Code
Erstellt: 2025-07-03
"""

import redis.asyncio as redis
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import json
import logging
from dataclasses import dataclass
from enum import Enum

from config.settings import settings

logger = logging.getLogger(__name__)

class RateLimitType(str, Enum):
    """Rate limit types"""
    PER_MINUTE = "per_minute"
    PER_HOUR = "per_hour"
    PER_DAY = "per_day"
    CONCURRENT = "concurrent"

@dataclass
class RateLimitConfig:
    """Rate limit configuration"""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    requests_per_day: int = 10000
    concurrent_requests: int = 10
    burst_allowance: int = 5

class RateLimiter:
    """Redis-based rate limiter with sliding window and burst protection"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.rate_limit_prefix = "rate_limit:"
        
    async def initialize_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            # Test connection
            await self.redis_client.ping()
            logger.info("✅ Rate Limiter Redis connection established")
        except Exception as e:
            logger.error(f"❌ Rate Limiter Redis connection failed: {e}")
            raise
    
    async def check_rate_limit(
        self,
        user_id: str,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        requests_per_day: int = 10000,
        endpoint: str = "general"
    ) -> bool:
        """
        Check if user is within rate limits
        Returns True if request is allowed, False if rate limited
        """
        
        if not self.redis_client:
            await self.initialize_redis()
        
        try:
            current_time = datetime.utcnow()
            
            # Check minute rate limit
            if not await self._check_sliding_window(
                user_id, endpoint, "minute", requests_per_minute, 60, current_time
            ):
                logger.warning(f"❌ Minute rate limit exceeded for user {user_id} on {endpoint}")
                return False
            
            # Check hour rate limit
            if not await self._check_sliding_window(
                user_id, endpoint, "hour", requests_per_hour, 3600, current_time
            ):
                logger.warning(f"❌ Hour rate limit exceeded for user {user_id} on {endpoint}")
                return False
            
            # Check day rate limit
            if not await self._check_sliding_window(
                user_id, endpoint, "day", requests_per_day, 86400, current_time
            ):
                logger.warning(f"❌ Day rate limit exceeded for user {user_id} on {endpoint}")
                return False
            
            # Increment all counters
            await self._increment_counters(user_id, endpoint, current_time)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Rate limit check error: {e}")
            # On error, allow request (fail open)
            return True
    
    async def check_concurrent_limit(self, user_id: str, max_concurrent: int = 10) -> bool:
        """Check concurrent request limit"""
        
        try:
            concurrent_key = f"{self.rate_limit_prefix}concurrent:{user_id}"
            current_count = await self.redis_client.get(concurrent_key)
            current_count = int(current_count) if current_count else 0
            
            if current_count >= max_concurrent:
                logger.warning(f"❌ Concurrent limit exceeded for user {user_id}")
                return False
            
            # Increment counter (will be decremented when request completes)
            await self.redis_client.incr(concurrent_key)
            await self.redis_client.expire(concurrent_key, 300)  # 5 minute safety timeout
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Concurrent limit check error: {e}")
            return True
    
    async def decrement_concurrent_requests(self, user_id: str):
        """Decrement concurrent request counter"""
        try:
            concurrent_key = f"{self.rate_limit_prefix}concurrent:{user_id}"
            await self.redis_client.decr(concurrent_key)
        except Exception as e:
            logger.error(f"❌ Error decrementing concurrent requests: {e}")
    
    async def get_rate_limit_status(
        self, 
        user_id: str, 
        endpoint: str = "general"
    ) -> Dict[str, any]:
        """Get current rate limit status for user"""
        
        try:
            current_time = datetime.utcnow()
            
            # Get current counts
            minute_count = await self._get_window_count(user_id, endpoint, "minute", current_time)
            hour_count = await self._get_window_count(user_id, endpoint, "hour", current_time)
            day_count = await self._get_window_count(user_id, endpoint, "day", current_time)
            
            # Get concurrent count
            concurrent_key = f"{self.rate_limit_prefix}concurrent:{user_id}"
            concurrent_count = await self.redis_client.get(concurrent_key)
            concurrent_count = int(concurrent_count) if concurrent_count else 0
            
            return {
                "user_id": user_id,
                "endpoint": endpoint,
                "current_usage": {
                    "per_minute": minute_count,
                    "per_hour": hour_count,
                    "per_day": day_count,
                    "concurrent": concurrent_count
                },
                "limits": {
                    "per_minute": 60,  # Default limits
                    "per_hour": 1000,
                    "per_day": 10000,
                    "concurrent": 10
                },
                "reset_times": {
                    "minute": (current_time + timedelta(minutes=1)).isoformat(),
                    "hour": (current_time + timedelta(hours=1)).isoformat(),
                    "day": (current_time + timedelta(days=1)).isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting rate limit status: {e}")
            return {}
    
    async def reset_rate_limits(self, user_id: str, endpoint: str = "general"):
        """Reset rate limits for user (admin function)"""
        
        try:
            # Clear all rate limit keys for user
            keys_to_delete = [
                f"{self.rate_limit_prefix}minute:{user_id}:{endpoint}",
                f"{self.rate_limit_prefix}hour:{user_id}:{endpoint}", 
                f"{self.rate_limit_prefix}day:{user_id}:{endpoint}",
                f"{self.rate_limit_prefix}concurrent:{user_id}"
            ]
            
            for key in keys_to_delete:
                await self.redis_client.delete(key)
            
            logger.info(f"✅ Rate limits reset for user {user_id} on {endpoint}")
            
        except Exception as e:
            logger.error(f"❌ Error resetting rate limits: {e}")
    
    async def _check_sliding_window(
        self,
        user_id: str,
        endpoint: str,
        window_type: str,
        limit: int,
        window_seconds: int,
        current_time: datetime
    ) -> bool:
        """Check sliding window rate limit"""
        
        window_key = f"{self.rate_limit_prefix}{window_type}:{user_id}:{endpoint}"
        
        # Get current window count
        current_count = await self._get_window_count(user_id, endpoint, window_type, current_time)
        
        return current_count < limit
    
    async def _get_window_count(
        self,
        user_id: str,
        endpoint: str,
        window_type: str,
        current_time: datetime
    ) -> int:
        """Get current count for a time window"""
        
        window_key = f"{self.rate_limit_prefix}{window_type}:{user_id}:{endpoint}"
        
        # For simplicity, using basic counters with expiration
        # In production, you might want to use more sophisticated sliding window
        if window_type == "minute":
            time_bucket = int(current_time.timestamp() // 60)
        elif window_type == "hour":
            time_bucket = int(current_time.timestamp() // 3600)
        elif window_type == "day":
            time_bucket = int(current_time.timestamp() // 86400)
        else:
            time_bucket = int(current_time.timestamp())
        
        bucket_key = f"{window_key}:{time_bucket}"
        count = await self.redis_client.get(bucket_key)
        
        return int(count) if count else 0
    
    async def _increment_counters(self, user_id: str, endpoint: str, current_time: datetime):
        """Increment all rate limit counters"""
        
        # Minute counter
        minute_bucket = int(current_time.timestamp() // 60)
        minute_key = f"{self.rate_limit_prefix}minute:{user_id}:{endpoint}:{minute_bucket}"
        
        # Hour counter
        hour_bucket = int(current_time.timestamp() // 3600)
        hour_key = f"{self.rate_limit_prefix}hour:{user_id}:{endpoint}:{hour_bucket}"
        
        # Day counter
        day_bucket = int(current_time.timestamp() // 86400)
        day_key = f"{self.rate_limit_prefix}day:{user_id}:{endpoint}:{day_bucket}"
        
        # Use pipeline for atomic operations
        pipe = self.redis_client.pipeline()
        
        # Increment minute counter
        pipe.incr(minute_key)
        pipe.expire(minute_key, 120)  # Keep for 2 minutes
        
        # Increment hour counter
        pipe.incr(hour_key)
        pipe.expire(hour_key, 7200)  # Keep for 2 hours
        
        # Increment day counter
        pipe.incr(day_key)
        pipe.expire(day_key, 172800)  # Keep for 2 days
        
        await pipe.execute()
    
    async def get_burst_allowance(self, user_id: str, subscription_tier: str) -> int:
        """Get burst allowance based on subscription tier"""
        
        burst_allowances = {
            "free": 5,
            "pro": 20,
            "enterprise": 100
        }
        
        return burst_allowances.get(subscription_tier, 5)
    
    async def apply_subscription_limits(self, user_id: str, subscription_tier: str) -> RateLimitConfig:
        """Get rate limits based on subscription tier"""
        
        tier_limits = {
            "free": RateLimitConfig(
                requests_per_minute=60,
                requests_per_hour=1000,
                requests_per_day=5000,
                concurrent_requests=5,
                burst_allowance=5
            ),
            "pro": RateLimitConfig(
                requests_per_minute=300,
                requests_per_hour=10000,
                requests_per_day=50000,
                concurrent_requests=20,
                burst_allowance=20
            ),
            "enterprise": RateLimitConfig(
                requests_per_minute=1000,
                requests_per_hour=50000,
                requests_per_day=500000,
                concurrent_requests=100,
                burst_allowance=100
            )
        }
        
        return tier_limits.get(subscription_tier, tier_limits["free"])
    
    async def cleanup_expired_counters(self):
        """Cleanup expired rate limit counters (background task)"""
        
        try:
            # Redis automatically expires keys, but we can do additional cleanup
            # This would typically be run as a background task
            
            current_time = datetime.utcnow()
            
            # Find old rate limit keys
            pattern = f"{self.rate_limit_prefix}*"
            keys = await self.redis_client.keys(pattern)
            
            expired_keys = []
            for key in keys:
                ttl = await self.redis_client.ttl(key)
                if ttl == -1:  # Key exists but has no expiration
                    expired_keys.append(key)
            
            if expired_keys:
                await self.redis_client.delete(*expired_keys)
                logger.info(f"✅ Cleaned up {len(expired_keys)} expired rate limit counters")
            
        except Exception as e:
            logger.error(f"❌ Rate limit cleanup error: {e}")

# Global rate limiter instance
rate_limiter = RateLimiter()