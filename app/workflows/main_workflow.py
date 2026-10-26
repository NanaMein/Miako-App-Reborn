import asyncio

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential

from ..core.config import settings_dev

azure_client = FoundryChatClient(
    project_endpoint=settings_dev.azure_project_endpoint,
    model="DeepSeek-V4-Flash",
    credential=DefaultAzureCredential()
)

agent = Agent(
    client=azure_client,
    instructions="You are a helpful AI assistant. Answer user questions accurately and concisely.",
)

async def main():
    response = await agent.run("Hello there!")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
