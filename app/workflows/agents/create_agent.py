from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentVersionDetails, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from frontmatter import load as markdown_loader
from pydantic import BaseModel, Field, ValidationError

from app.core.config import settings_dev

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


def create_prompt_agent_foundry(filename: str) -> AgentVersionDetails | None:
    agent_config = get_local_agent_config(filename=filename)
    if not agent_config:
        return None

    with AIProjectClient(
        credential=DefaultAzureCredential(),
        endpoint=settings_dev.azure_project_endpoint
    ) as client:
        return client.agents.create_version(
            agent_name=agent_config.agent_name,
            definition=PromptAgentDefinition(
                model=agent_config.model,
                instructions=agent_config.instructions
            )
        )
