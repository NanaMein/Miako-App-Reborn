from redis.asyncio import Redis
from cachetools import TTLCache
from asyncio import Lock
from json import dumps, loads

class BaseAsyncRedisRepository:
    def __init__(self, url: str):
        self.redis = Redis.from_url(url)


class ShortMemoryMessageRepository:
    pass

class ShortMemoryRepository:
    _ttl_cache: TTLCache[str, str] = TTLCache(maxsize=1000, ttl=3600)
    _lock_cache: TTLCache[str, Lock] = TTLCache(maxsize=1000, ttl=3600)
    _main_lock: Lock = Lock()

    @classmethod
    async def get_lock(cls, key: str) -> Lock:
        current_lock = cls._lock_cache.get(key)
        if current_lock is None:
            async with cls._main_lock:
                lock = Lock()
                cls._lock_cache[key] = lock
                return lock
        return current_lock
            
    async def _add(self, key: str, value: str) -> str:
        lock = await self.get_lock(key=key)
        async with lock:
            self._ttl_cache[key] = value
            return value

    async def _get(self, key: str) -> str | None:
        return self._ttl_cache.get(key)

    async def add_user_message(self, user_id: str, content: str):
        try:
            current_messages = await self._get(key=user_id)
            new_user_message = {"role":"user","content":content}
            
            if current_messages is not None:
                temp_messages: list[dict] = loads(current_messages)
                temp_messages.append(new_user_message)
                transformed_messages = dumps(temp_messages)
                await self._add(key=user_id, value=transformed_messages)
                return True
                
            first_new_message = [new_user_message]
            await self._add(key=user_id, value=dumps(first_new_message))
            return True
        except Exception:
            return False

    async def add_assistant_message(self, user_id: str, content: str):
        try:
            current_messages = await self._get(key=user_id)
            new_user_message = {"role":"assistant","content":content}
            
            if current_messages is not None:
                temp_messages: list[dict] = loads(current_messages)
                temp_messages.append(new_user_message)
                transformed_messages = dumps(temp_messages)
                await self._add(key=user_id, value=transformed_messages)
                return True
                
            first_new_message = [new_user_message]
            await self._add(key=user_id, value=dumps(first_new_message))
            return True
        except Exception:
            return False

    