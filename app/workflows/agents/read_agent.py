from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentVersionDetails
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from frontmatter import load as markdown_loader
from pydantic import BaseModel, Field, ValidationError

from ...core.config import settings_dev

PROMPT_DIR = Path(__file__).parent.parent

class AgentConfig(BaseModel):
    agent_name: str = Field(description="Name of the agent")
    model: str = Field(description="Name of the model")
    instructions: str = Field(description="The system prompt and instructions of the agent")

def file_name_to_path(name: str) -> Path:
    return PROMPT_DIR / "prompts" / f"{name}.md"

def load_path_to_prompts(path: Path) -> AgentConfig | None:
    post = markdown_loader(fd=path)
    try:
        return AgentConfig(
            agent_name=post.get("agent_name"),
            model=post.get("model"),
            instructions=post.content.strip()
        )
    except ValidationError:
        return None

def get_local_agent_config(filename: str) -> AgentConfig | None:
    agent_prompt_path = file_name_to_path(name=filename)
    return load_path_to_prompts(path=agent_prompt_path)

def read_prompt_agent_foundry(agent_name: str, agent_version: str = "1") -> AgentVersionDetails | None:
    with AIProjectClient(
        credential=DefaultAzureCredential(),
        endpoint=settings_dev.azure_project_endpoint
    ) as client:
        try:
            return client.agents.get_version(agent_name=agent_name, agent_version=agent_version)
        except HttpResponseError as e:
            if e.status_code == 404:
                return None  # Agent does not exist in Foundry
            raise  # Re-raise other API errors


