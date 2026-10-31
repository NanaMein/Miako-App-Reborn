from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_azure_ai_search import AzureAISearchContextProvider
from azure.identity import DefaultAzureCredential
from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.config import settings_dev
from ..workflows.tools import translator_tool

chat_router = APIRouter()

search_provider = AzureAISearchContextProvider(
    endpoint=settings_dev.azure_search_endpoint,
    index_name="testing-index-name",
    credential=DefaultAzureCredential(),
    mode="semantic"
)

azure_client = FoundryChatClient(
    project_endpoint=settings_dev.azure_project_endpoint,
    model="DeepSeek-V4-Flash",
    credential=DefaultAzureCredential()
)

agent = Agent(
    client=azure_client,
    instructions="You are a helpful AI assistant. Answer user questions accurately and concisely.",
    context_providers=[search_provider]
)


class Chat(BaseModel):
    message: str = Field(default="", description="Message input and output from chat agent.")


@chat_router.post("/chat")
async def chat_agent(chat: Chat):
    english_message = translator_tool(chat.message)
    agent_response = await agent.run(english_message)
    translated_response = translator_tool(
        query=agent_response.text,
        input_lang="en",
        output_lang="fil"
    )
    return Chat(message=translated_response)
    
    
