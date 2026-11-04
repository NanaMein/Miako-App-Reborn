
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import DefaultAzureCredential

from ...core.config import settings_dev


class AzureAIException(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code
        

class AzureAIProjectService:
    def __init__(self):
        self._credential: DefaultAzureCredential | None = None
        self._client: AIProjectClient | None = None

    @property
    def client(self):
        if self._client:
            return self._client
        raise AzureAIException("Azure AI Project Client not yet initialized.")

    @property
    def credential(self):
        if self._credential:
            return self._credential
        raise AzureAIException("Default Azure Credential is not yet initialized.")

    async def start(self):
        if not self._credential:
            self._credential = DefaultAzureCredential()
        if not self._client:
            self._client = AIProjectClient(
                credential=self._credential,
                endpoint=settings_dev.azure_project_endpoint
            )

    async def stop(self):
        if self._credential:
            await self._credential.close()
        if self._client:
            await self._client.close()


ai_service = AzureAIProjectService()