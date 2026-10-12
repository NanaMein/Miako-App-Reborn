import os
from asyncio import Lock
from json import dumps, loads
from typing import Literal

from cachetools import TTLCache
from langchain_cohere import CohereEmbeddings
from mem0 import AsyncMemory
from redis.asyncio import Redis

from ...core.config import settings


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

    async def _add_message(self, user_id: str, role: str, content: str) -> bool:
        try:
            if role not in ["user", "assistant"]:
                return False
            current_messages = await self._get(key=user_id)
            new_user_message = {"role":role,"content":content}
            
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


    async def add_user_message(self, user_id: str, content: str):
        return await self._add_message(user_id=user_id, role="user", content=content)


    async def add_assistant_message(self, user_id: str, content: str):
        return await self._add_message(user_id=user_id, role="assistant", content=content)


os.environ["COHERE_API_KEY"] = settings.cohere_api_key
os.environ["GROQ_API_KEY"] = settings.groq_api_key


class LongMemoryRepository:
    _mem_zero_config: dict | None = None
    _async_memory_client: AsyncMemory | None = None


    @classmethod
    def get_config_parameter(cls) -> dict[str, dict[str, str | dict[str, str | int]] | dict[str, str | dict[str, str | float]] | dict[str, str | dict[str, CohereEmbeddings]]]:
        if cls._mem_zero_config is None:
            cls._mem_zero_config = {
                "vector_store": {
                    "provider": "milvus",
                    "config": {
                        "url": settings.milvus_config["uri"],
                        "token": settings.milvus_config["token"],
                        "collection_name": settings.milvus_config["collection_name"],
                        "embedding_model_dims": 1536,
                    }
                },
                "llm": {
                    "provider":"groq",
                    "config": {
                        "model":"openai/gpt-oss-120b",
                        "temperature": 0.3,
                        "max_tokens": 10_000,
                        "reasoning_effort": "medium",
                    }
                },
                "embedder": {
                    "provider": "langchain",
                    "config": {
                        "model": CohereEmbeddings(
                            model="embed-v4.0",
                            client=None,
                            async_client=None
                        )  
                    }
                }
            }
        return cls._mem_zero_config
    

    @classmethod
    def init_memory_client(cls):
        if cls._async_memory_client is None:
            config_dict = cls.get_config_parameter()
            cls._async_memory_client = AsyncMemory.from_config(config_dict=config_dict)

    @classmethod
    def close_memory_client(cls):
        if cls._async_memory_client:
            cls._async_memory_client.close()
            cls._async_memory_client = None

    @property
    def memory_client(self) -> AsyncMemory:
        if self._async_memory_client is None:
            raise RuntimeError("Memory client not initialized")
        return self._async_memory_client

    async def add_memory(self, user_id: str, content: str):
        await self.memory_client.add(user_id=user_id, messages=content)

    async def search_memory(
        self, 
        user_id: str, 
        content: str,
        output: Literal["str", "raw"] = "str",
        **kwargs
    ) -> str | list[dict]:
        results = await self.memory_client.search(query=content, filters={"user_id": user_id}, **kwargs)
        cleaned_data = self.cleaned_searched_result(search_results=results)
        if output == "str":
            return dumps(cleaned_data)
        return cleaned_data

    async def full_search_memory(
        self,
        user_id: str,
        query: str,
        output: Literal["str", "raw"] = "str",
        explain: bool = False,
    ) -> str | dict:

        results = await self.memory_client.search(
            query=query,
            filters={"user_id": user_id},
            explain=explain
        )
        if output == "str":
            return dumps(results)
        return results

    @staticmethod
    def cleaned_searched_result(search_results: dict[str, list[dict]]) -> list[dict]:
        allowed_fields = {
            "memory",
            "metadata",
            "score",
            "score_details",
            "created_at",
            "updated_at",
        }

        return [
            {key: value for key, value in sr.items() if key in allowed_fields}
            for sr in search_results.get("results", [])
        ]