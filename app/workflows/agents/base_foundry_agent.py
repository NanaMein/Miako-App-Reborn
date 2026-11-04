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
    _credential: DefaultAzureCredential | None = None
    _client: AIProjectClient | None = None

    @property
    def client(self):
        if self._client is None:
            raise AzureAIException("Azure AI Project Client not yet initialized.")
        return self._client

    @property
    def credential(self):
        if self._credential is None:
            raise AzureAIException("Default Azure Credential is not yet initialized.")
        return self._credential

    @classmethod
    async def start(cls):
        if cls._credential is None:
            cls._credential = DefaultAzureCredential()
        if cls._client is None:
            cls._client = AIProjectClient(
                credential=cls._credential,
                endpoint=settings_dev.azure_project_endpoint
            )

    @classmethod
    async def stop(cls):
        if cls._credential is not None:
            await cls._credential.close()
        if cls._client is not None:
            await cls._client.close()

