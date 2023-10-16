from fastapi_redis_rate_limiter import RedisClient, RedisRateLimiterMiddleware
from app.settings import settings

# Initialize the Redis client
redis_client = RedisClient(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db
)
