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



settings = Settings()

class SettingsDeveloper:

    AZURE_PROJECT_ENDPOINT: str | None = os.getenv("AZURE_PROJECT_ENDPOINT", None)
    AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", None)
    AZURE_TRANSLATOR_DEPLOYMENT_NAME =  os.getenv("AZURE_TRANSLATOR_DEPLOYMENT_NAME", "gpt-5.6-luna")
    AZURE_TRANSLATOR_API_VERSION = os.getenv("AZURE_TRANSLATOR_API_VERSION","2026-06-06")
    AZURE_TRANSLATOR_KEY: str | None = os.getenv("AZURE_TRANSLATOR_KEY", None)

    
    def __init__(self):
        logger.info("Loading application Developer settings for testing purposes")

    @property
    def azure_project_endpoint(self):
        if not self.AZURE_PROJECT_ENDPOINT:
            raise RuntimeError("AZURE_PROJECT_ENDPOINT not set")
        return self.AZURE_PROJECT_ENDPOINT

    @property
    def azure_translator_url(self):
        if not self.AZURE_TRANSLATOR_ENDPOINT and not self.AZURE_TRANSLATOR_API_VERSION:
            raise RuntimeError("AZURE_TRANSLATOR_ENDPOINT and AZURE_TRANSLATOR_API_VERSION not set")
        return f"{self.AZURE_TRANSLATOR_ENDPOINT}/translator/text/translate?api-version={self.AZURE_TRANSLATOR_API_VERSION}"

    @property
    def azure_translator_headers(self):
        if not self.AZURE_TRANSLATOR_KEY:
            raise RuntimeError("AZURE_TRANSLATOR_KEY not set")
        return {
            "Ocp-Apim-Subscription-Key": self.AZURE_TRANSLATOR_KEY,
            "Content-Type": "application/json",
        }

    @property
    def azure_translator_deployment_name(self):
        return self.AZURE_TRANSLATOR_DEPLOYMENT_NAME

    @property
    def azure_search_endpoint(self):
        return os.getenv("AZURE_SEARCH_ENDPOINT", None)





settings_dev = SettingsDeveloper()