from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import DeleteAgentResponse
from azure.identity import DefaultAzureCredential

from ...core.config import settings_dev
from .create_agent import AgentConfig, get_local_agent_config


def delete_prompt_agent_foundry(filename: str) -> bool:
    agent_config: AgentConfig | None = get_local_agent_config(filename=filename)
    if not agent_config:
        return False
    try:
        with AIProjectClient(
            endpoint=settings_dev.azure_project_endpoint,
            credential=DefaultAzureCredential()
        ) as client:
            deleted_agent: DeleteAgentResponse = client.agents.delete(agent_name=agent_config.agent_name)
            print(deleted_agent.as_dict())
            return True
    except Exception as ex:
        print(f"Error delete: {ex!s}")
        return False

