from pathlib import Path

import frontmatter
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import DefaultAzureCredential
from pydantic import BaseModel, Field, ValidationError

from ...core.config import settings_dev

SAMPLE_AGENT_FILENAME = "MiraiAikoAgent"

class AzureAIException(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code
        



class AgentConfigResult(BaseModel):
    agent_name: str = Field(description="Name of the agent")
    model: str = Field(description="Name of the model")
    instructions: str = Field(description="The system prompt and instructions of the agent")

class AgentConfigService:
    prompt_dir: Path = Path(__file__).parent.parent

    def _filename_to_prompt_path(self, filename: str) -> Path:
        return self.prompt_dir / "prompts" / f"{filename}.md"

    def _markdown_loader(self, fd: Path) -> frontmatter.Post:
        return frontmatter.load(fd=fd)
        
    def _load_prompts(self, post: frontmatter.Post) -> AgentConfigResult | None:
        try:
            return AgentConfigResult(
                agent_name=post.get("agent_name"),
                model=post.get("model"),
                instructions=post.content.strip()
            )
        except ValidationError:
            return None
    
    def get_agent_config_result(self, filename: str) -> AgentConfigResult | None:
        prompt_path = self._filename_to_prompt_path(filename=filename)
        post = self._markdown_loader(fd=prompt_path)
        extracted_prompt = self._load_prompts(post=post)
        if extracted_prompt:
            return extracted_prompt
        raise AzureAIException("No Agent Config found", status_code=404)



        
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