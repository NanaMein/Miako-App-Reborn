# Mirai Aiko (Reborn)

**A text-first AI companion with the goal of understanding Taglish, modern Filipino slang, and language-switching in context.**

Mirai Aiko Reborn is an updated, refactored continuation of my original Miako project—not a brand-new project. The idea grew out of my experience abroad; I’ll share the fuller story another time. This README describes the current learning prototype, the direction I’m working toward, and the boundaries between them.

## Product goal and priorities

Mirai Aiko is intended for people who speak Taglish, use modern Filipino and Gen Z slang, switch languages mid-thought, or otherwise communicate in ways that English-first AI systems can misunderstand. It should follow meaning and conversational context through language and topic shifts, then respond naturally in the language mix and style that fits.

The work is intentionally staged:

1. **Language understanding and context:** build and evaluate reliable understanding of Taglish, code-switching, slang, follow-ups, and topic changes.
2. **Cost-effective conversations:** use model and context choices that meet quality goals without requiring a high-reasoning frontier model for every interaction; measure quality and cost rather than assume either.
3. **Tools and automation:** consider agent tools and workflow automation such as n8n only after the first two priorities have solid implementations and pass their evaluations.

This is a text-only project for now. Voice input and output are not in the current plan.

## Primary foundation: Microsoft Agent Framework and Azure AI Foundry

**Microsoft Agent Framework (MAF) is the primary agent-framework direction. Azure AI Foundry is the project’s main model and agent platform while I learn and build this system.** Azure is the current focus, not an irreversible commitment that prevents revisiting providers later. The goal is to grow the workflow incrementally, with clearer boundaries among workflows, services, and repositories under `app/` as the implementation needs them. The current small workflow is a learning and testing scaffold; it is not meant to prescribe the final architecture.

This project also supports my current Azure AI-901 and AI-103 learning goals; learning informs the design, while implementation choices will follow the project’s needs and evaluation results.

### What is currently implemented

The running FastAPI app currently exposes a health check, cookie-based user-authentication routes, and a simple chat prototype:

```text
POST /api/chat
    │
    ▼
app/workflows/main_workflow.py
    │  Translate Filipino input to English
    │  Run one MAF Agent through FoundryChatClient
    │  Translate the English response back to Filipino
    ▼
JSON response: {"message": "..."}
```

The current Foundry client is configured for `DeepSeek-V4-Flash`. The translation helper lives in `app/workflows/tools.py`; it is called by the workflow and is not currently registered as an agent tool. This is a straightforward Filipino-to-English-to-Filipino test path, **not** the planned Taglish/Gen Z language-understanding pipeline. The chat route does not currently apply the existing cookie-auth dependency, so treat it as an experimental endpoint rather than a production-ready authenticated chat API.

The chat response is ordinary JSON. Streaming is deliberately off for now while I learn how a future MAF workflow should be designed. No streaming, SSE layer, or message broker is part of the current chat path.

Other currently wired behavior:

- `GET /health-check` reports API health.
- User-authentication endpoints are mounted under `/api/auth`.
- Redis currently supports authentication tokens; it does not yet store chat history.
- MongoDB currently supports user persistence; it is not yet being used for chat memory.
- There is no connected Taglish interpretation pipeline, bounded conversation-history feature, long-term semantic memory, or multi-agent/tool orchestration in the running chat workflow.

### Intended MAF and Foundry workflow

The following is a direction for gradual implementation, not a description of features that are already wired into the API:

1. **FastAPI application layer:** receive and validate a normal REST request and coordinate the workflow. Keep new responsibilities in appropriate parts of `app/` as they become necessary instead of over-building the initial prototype.
2. **MAF orchestration with Azure AI Foundry:** develop language understanding that can preserve the user’s meaning across Taglish, code-switching, slang, and topic shifts. A validated internal handoff may capture language, intent, entities, constraints, uncertainty, and ambiguities that need clarification. This internal representation should help reasoning without forcing the final reply into a rigid style.
3. **Conversation context and memory:** a bounded recent-context window and longer-term semantic recall are possible future capabilities. Redis currently serves auth tokens only; chat history and semantic memory are not implemented. Select a memory or RAG approach only when the use case is clear, and keep retrieved memories as supporting context rather than instructions that override the user’s request.
4. **Natural response:** aim for a clear, useful answer in a language mix and tone appropriate to the user. The present translation loop is only a test implementation and should not be mistaken for that capability.
5. **Normal REST first:** continue returning standard JSON while learning and evaluating the workflow. Streaming can be reconsidered later when the MAF design and response transport are clearer.

## Future supporting options—not current dependencies or commitments

The core direction remains MAF with Azure AI Foundry as the current platform focus. Other products and frameworks may be evaluated as supporting integrations or alternatives when a specific need arises; none of these are part of the current installed project stack or a promise to adopt them:

- **LlamaIndex** for a future RAG implementation when more control is needed.
- **Mem0** for a possible more abstracted memory layer.
- **CrewAI** for a possible alternate or supporting multi-agent framework.
- **LangChain** for its broader integrations and AI-tool ecosystem.
- **n8n** for future workflow automation, after language/context quality and cost goals have been implemented and evaluated.

These options do not replace the present MAF-first learning path by default. Add technology only when the project has a concrete requirement for it.

## Current project status

This repository is an early foundation, not a finished or production-ready assistant. It currently wires FastAPI, user authentication, MongoDB and Redis startup, and the simple MAF/Foundry chat prototype described above. The core product goals—robust Taglish and Gen Z slang understanding, context handling, measured low-cost conversations, and evaluations—remain work to do. Long-term memory, RAG, multi-agent collaboration, agent tool use, and automation are future extensions rather than current capabilities.

## Running the current API

The project uses Python 3.13 and `uv`. Run commands from the repository root. Configuration loads `.env` from the process working directory. The current app needs `MONGO_URI` and `REDIS_URI` for database/cache startup, and `AZURE_PROJECT_ENDPOINT` because the Foundry client is constructed during module import. The chat request additionally needs credentials available to `DefaultAzureCredential` and Azure Translator configuration (`AZURE_TRANSLATOR_ENDPOINT` and `AZURE_TRANSLATOR_KEY`). Keep credentials in your local environment; do not commit secrets.

```bash
uv sync
uv run python main.py
```

The current Docker Compose file starts MongoDB and Redis and maps the backend to `127.0.0.1:8000`:

```bash
docker compose up --build
```

Compose currently passes MongoDB and Redis settings to the backend, but not `AZURE_PROJECT_ENDPOINT`. Since the app accesses that setting while importing the Foundry workflow, the backend needs that Azure setting supplied to its container or it can fail before the health, auth, or chat routes are available. The Compose configuration is not changed by these instructions.

When running, the API is available at `http://localhost:8000`; its health endpoint is `/health-check`, authentication routes are under `/api/auth`, and the current chat prototype is `POST /api/chat`.

## License

MIT
