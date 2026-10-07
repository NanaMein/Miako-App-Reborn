from pydantic import BaseModel, Field

from crewai.flow.flow import Flow, start, listen


class MessageInput(BaseModel):
    id: str | None = Field(default=None)
    message: str | None = Field(default=None)
    short_memory_list: list[dict] | None = Field(default=None)
    long_memory_context: str | None = Field(default=None)


class AppWorkflow(Flow[MessageInput]):

    @start()
    async def start_flow(self):
        pass
        