from agent_framework.foundry import FoundryChatClient
from agent_framework import Agent
from azure.identity import DefaultAzureCredential
import asyncio




azure_client = FoundryChatClient(
    project_endpoint="Insert-project-endpoint-here",
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
