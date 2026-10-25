import os
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class Settings:
    MONGO_URI: str | None = os.getenv("MONGO_URI", None)
    REDIS_URI: str | None = os.getenv("REDIS_URI", None)
    PH_TZ: ZoneInfo = ZoneInfo("Asia/Manila")
    IS_DEPLOYED_FOR_PRODUCTION: bool = os.getenv("IS_DEPLOYED_FOR_PRODUCTION", "false").lower() == "true"
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY", None)
    COHERE_API_KEY: str | None = os.getenv("COHERE_API_KEY", None)
    MILVUS_URI: str | None = os.getenv("MILVUS_URI", None)
    MILVUS_TOKEN: str | None = os.getenv("MILVUS_TOKEN", None)
    MILVUS_COLLECTION_NAME: str | None = os.getenv("MILVUS_COLLECTION_NAME", None)

    def __init__(self):
        logger.info("Loading application settings")
        
    @property
    def ph_tz(self) -> ZoneInfo:
        try:
            return self.PH_TZ
        except ZoneInfoNotFoundError:
            return ZoneInfo("Asia/Manila")

    @property
    def is_deployed_for_production(self) -> bool:
        return self.IS_DEPLOYED_FOR_PRODUCTION


    @property
    def mongo_uri(self) -> str:
        if not self.MONGO_URI:
            raise RuntimeError("MONGO_URI not set")
        return self.MONGO_URI

    @property
    def redis_uri(self) -> str:
        if not self.REDIS_URI:
            raise RuntimeError("REDIS_URI not set")
        return self.REDIS_URI

    @property
    def groq_api_key(self) -> str:
        if not self.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY not set")
        return self.GROQ_API_KEY

    @property
    def cohere_api_key(self) -> str:
        if not self.COHERE_API_KEY:
            raise RuntimeError("COHERE_API_KEY not set")
        return self.COHERE_API_KEY

    @property
    def milvus_uri(self) -> str:
        if not self.MILVUS_URI:
            raise RuntimeError("MILVUS_URI not set")
        return self.MILVUS_URI

    @property
    def milvus_token(self) -> str:
        if not self.MILVUS_TOKEN:
            raise RuntimeError("MILVUS_TOKEN not set")
        return self.MILVUS_TOKEN

    @property
    def milvus_collection_name(self) -> str:
        if not self.MILVUS_COLLECTION_NAME:
            raise RuntimeError("MILVUS_COLLECTION_NAME not set")
        return self.MILVUS_COLLECTION_NAME

    @property
    def milvus_config(self) -> dict[str, str]:
        return {
            "uri": self.milvus_uri,
            "token": self.milvus_token,
            "collection_name": self.milvus_collection_name,
        }


settings = Settings()

class SettingsDeveloper:
    def __init__(self):
        logger.info("Loading application Developer settings for testing purposes")
        
    AZURE_TRANSLATE_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
    AZURE_TRANSLATE_KEY: str | None = os.getenv("AZURE_TRANSLATE_KEY", None)
    AZURE_TRANSLATE_LOCATION: str | None = os.getenv("AZURE_TRANSLATE_LOCATION", None)
    AZURE_TRANSLATE_PATH = "/translate"

    AZURE_PROJECT_ENDPOINT: str | None = os.getenv("AZURE_PROJECT_ENDPOINT", None)


    @property
    def azure_translate_key(self) -> str:
        if not self.AZURE_TRANSLATE_KEY:
            raise RuntimeError("AZURE_TRANSLATE_KEY not set")
        return self.AZURE_TRANSLATE_KEY

    @property
    def azure_translate_location(self) -> str:
        if not self.AZURE_TRANSLATE_LOCATION:
            raise RuntimeError("AZURE_TRANSLATE_LOCATION not set")
        return self.AZURE_TRANSLATE_LOCATION

    @property
    def azure_translate_url(self) -> str:
        if not self.AZURE_TRANSLATE_ENDPOINT and not self.AZURE_TRANSLATE_PATH:
            raise RuntimeError("AZURE_TRANSLATE_ENDPOINT and AZURE_TRANSLATE_PATH not set")
        return self.AZURE_TRANSLATE_ENDPOINT + self.AZURE_TRANSLATE_PATH

    @property
    def azure_project_endpoint(self):
        if not self.AZURE_PROJECT_ENDPOINT:
            raise RuntimeError("AZURE_PROJECT_ENDPOINT not set")
        return self.AZURE_PROJECT_ENDPOINT
    

settings_dev = SettingsDeveloper()