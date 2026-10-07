from app_orig_copy.repositories.in_memory_database.redis_repository import RedisAsyncRepository
from redis.asyncio import Redis


class BaseAsyncRedisRepository:
    def __init__(self, url: str):
        self.redis = Redis.from_url(url)


class ShortMemoryMessageRepository: