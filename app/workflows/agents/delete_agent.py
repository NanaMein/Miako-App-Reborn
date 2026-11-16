from .base_foundry_agent import AzureAIProjectService


class DeleteAgent:
    def __init__(self, name: str, version: str | None = None):
        self._name = name
        self._version = version
        self._azure_ai_service: AzureAIProjectService | None = None

    @property
    def azure_ai_service(self) -> AzureAIProjectService:
        if self._azure_ai_service is None:
            self._azure_ai_service = AzureAIProjectService()
        return self._azure_ai_service
        
    async def run(self):
        return await self.azure_ai_service.delete_prompt_agent(
            name=self._name,
            agent_version=self._version or "1"
        )
