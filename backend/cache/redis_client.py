"""
Redis cache client for NoaMetrics
"""
import os
import json
import logging
from typing import Optional, Any, Union, Dict, List
from datetime import datetime, timedelta
import redis
from redis.connection import ConnectionPool
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis cache client with connection pooling and automatic serialization"""
    
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.pool = None
        self.client = None
        self._setup_connection()
    
    def _setup_connection(self):
        """Setup Redis connection with pooling"""
        try:
            self.pool = ConnectionPool.from_url(
                self.redis_url,
                max_connections=20,
                retry_on_timeout=True,
                socket_keepalive=True,
                socket_keepalive_options={},
                health_check_interval=30
            )
            self.client = redis.Redis(connection_pool=self.pool)
            
            # Test connection
            self.client.ping()
            logger.info("Redis connection established successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None
    
    def _serialize(self, value: Any) -> str:
        """Serialize value to JSON string"""
        if isinstance(value, (datetime, timedelta)):
            return json.dumps(value, default=str)
        return json.dumps(value)
    
    def _deserialize(self, value: str) -> Any:
        """Deserialize JSON string to Python object"""
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        if not self.client:
            return False
        try:
            self.client.ping()
            return True
        except:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache"""
        if not self.is_connected():
            return default
        
        try:
            value = self.client.get(key)
            if value is None:
                return default
            if isinstance(value, bytes):
                return self._deserialize(value.decode('utf-8'))
            return self._deserialize(str(value))
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return default
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set value in cache with optional expiration"""
        if not self.is_connected():
            return False
        
        try:
            serialized_value = self._serialize(value)
            if expire:
                return self.client.setex(key, expire, serialized_value)
            else:
                return self.client.set(key, serialized_value)
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False
    
    def setex(self, key: str, seconds: int, value: Any) -> bool:
        """Set value with expiration in seconds"""
        return self.set(key, value, expire=seconds)
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.is_connected():
            return False
        
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.is_connected():
            return False
        
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Error checking key {key}: {e}")
            return False
    
    def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for key"""
        if not self.is_connected():
            return False
        
        try:
            return self.client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Error setting expiration for key {key}: {e}")
            return False
    
    def ttl(self, key: str) -> int:
        """Get time to live for key"""
        if not self.is_connected():
            return -1
        
        try:
            return self.client.ttl(key)
        except Exception as e:
            logger.error(f"Error getting TTL for key {key}: {e}")
            return -1
    
    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment counter"""
        if not self.is_connected():
            return None
        
        try:
            return self.client.incr(key, amount)
        except Exception as e:
            logger.error(f"Error incrementing key {key}: {e}")
            return None
    
    def hget(self, name: str, key: str, default: Any = None) -> Any:
        """Get value from hash"""
        if not self.is_connected():
            return default
        
        try:
            value = self.client.hget(name, key)
            if value is None:
                return default
            return self._deserialize(value.decode('utf-8'))
        except Exception as e:
            logger.error(f"Error getting hash {name}:{key}: {e}")
            return default
    
    def hset(self, name: str, key: str, value: Any) -> bool:
        """Set value in hash"""
        if not self.is_connected():
            return False
        
        try:
            serialized_value = self._serialize(value)
            return bool(self.client.hset(name, key, serialized_value))
        except Exception as e:
            logger.error(f"Error setting hash {name}:{key}: {e}")
            return False
    
    def hgetall(self, name: str) -> Dict[str, Any]:
        """Get all values from hash"""
        if not self.is_connected():
            return {}
        
        try:
            result = self.client.hgetall(name)
            return {k.decode('utf-8'): self._deserialize(v.decode('utf-8')) 
                   for k, v in result.items()}
        except Exception as e:
            logger.error(f"Error getting hash {name}: {e}")
            return {}
    
    def lpush(self, name: str, *values: Any) -> Optional[int]:
        """Push values to list"""
        if not self.is_connected():
            return None
        
        try:
            serialized_values = [self._serialize(v) for v in values]
            return self.client.lpush(name, *serialized_values)
        except Exception as e:
            logger.error(f"Error pushing to list {name}: {e}")
            return None
    
    def lrange(self, name: str, start: int = 0, end: int = -1) -> List[Any]:
        """Get range from list"""
        if not self.is_connected():
            return []
        
        try:
            result = self.client.lrange(name, start, end)
            return [self._deserialize(v.decode('utf-8')) for v in result]
        except Exception as e:
            logger.error(f"Error getting list {name}: {e}")
            return []
    
    def flushdb(self) -> bool:
        """Clear all keys from current database"""
        if not self.is_connected():
            return False
        
        try:
            self.client.flushdb()
            return True
        except Exception as e:
            logger.error(f"Error flushing database: {e}")
            return False
    
    def info(self) -> Dict[str, Any]:
        """Get Redis server info"""
        if not self.is_connected():
            return {}
        
        try:
            return self.client.info()
        except Exception as e:
            logger.error(f"Error getting Redis info: {e}")
            return {}
    
    @contextmanager
    def pipeline(self):
        """Context manager for Redis pipeline"""
        if not self.is_connected():
            yield None
            return
        
        try:
            pipe = self.client.pipeline()
            yield pipe
            pipe.execute()
        except Exception as e:
            logger.error(f"Error in Redis pipeline: {e}")
            yield None
    
    def close(self):
        """Close Redis connection"""
        if self.client:
            self.client.close()
        if self.pool:
            self.pool.disconnect()
        logger.info("Redis connection closed")

# Global Redis cache instance
redis_cache = RedisCache()

# Cache decorators
def cached(expire: int = 3600):
    """Decorator to cache function results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = redis_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_cache.set(cache_key, result, expire=expire)
            return result
        return wrapper
    return decorator

def cache_key(prefix: str, expire: int = 3600):
    """Decorator with custom cache key prefix"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_key = f"{prefix}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            cached_result = redis_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            redis_cache.set(cache_key, result, expire=expire)
            return result
        return wrapper
    return decorator 