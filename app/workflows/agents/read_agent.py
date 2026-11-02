from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentVersionDetails
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential

from ...core.config import settings_dev


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


