# Mirai Aiko (Reborn)

**A text-first AI companion designed to understand Taglish, language-switching, and the way people actually talk.**

**Reborn** is an updated, refactored rework of my original Mirai Aiko project—not a brand-new project. It carries forward the earlier project’s foundation while reshaping it around the architecture and goals described here. The idea grew out of my experience abroad; I’ll share the fuller story another time. For now, this README focuses on the product goal and the system I want to build.

## The goal

Mirai Aiko is for people who speak Taglish, use modern Filipino and Gen Z slang, switch languages mid-thought, or otherwise communicate in ways that English-first AI systems can misunderstand. It should follow the user’s meaning and conversational context—even when the language or topic shifts—and return an answer that feels natural in the language and style they used.

The language-understanding layer is meant to identify intent and preserve meaning, not limit what the assistant can say. The response can still be fluent, flexible, and creative; the intermediate structure simply gives the rest of the system a clearer understanding of what the user meant.

The first version is **text-only**. Voice input and output are not part of the current plan.

## Intended architecture

This is the target design, not a claim that every stage is already implemented. FastAPI will be the application layer, with Azure AI Foundry as the model and agent-orchestration platform. Agent design will grow alongside my Azure AI-103 studies; specific models, agent roles, and Azure services remain implementation decisions.

```text
User message
    │
    ▼
FastAPI chat endpoint
    │  Authenticate, validate the request, and coordinate the response
    ▼
Redis short-term conversation context
    │  Keep a bounded, recent history for follow-ups and topic shifts
    ▼
Azure AI Foundry language understanding and agent orchestration
    │  Interpret code-switching, preserve intent, and coordinate specialized agents/tools
    ▼
Long-term semantic context
    │  Retrieve relevant user context; storage and Azure integration to be decided
    ▼
Response generation and language/style polish
    │  Produce a natural answer in the language mix and tone of the user's message
    ▼
FastAPI streams the response directly to the client
    │  HTTP streaming response; no message broker in the planned request path
    ▼
User
```

### 1. API and short-term conversation context — FastAPI and Redis

FastAPI will receive chat requests, apply the application’s authentication and validation, and coordinate the workflow. Redis will keep a small, bounded window of recent conversation. This gives the assistant nearby context for follow-ups and topic changes without treating the entire chat history as permanent memory. The size and expiry policy still need to be defined.

### 2. Language understanding and orchestration — Azure AI Foundry

For non-English and mixed-language input, an Azure AI Foundry model or agent will interpret the message and produce a validated structured representation for downstream reasoning. Depending on the message, that representation may include:

- Detected language or languages and a confidence score.
- A concise English interpretation that preserves the original meaning and context.
- Intent, relevant entities, and task constraints.
- Whether a workflow or tool may be appropriate, with a confidence or uncertainty signal.
- Ambiguities the next step should clarify rather than guess about.

This is an internal handoff format, not the final answer. The intent is to use Azure-hosted models to understand the user—not to depend on scraping or translating web content to interpret ordinary conversation. Structured output should be validated, and uncertainty should remain visible to later steps. Multi-agent roles and routing will be designed as the Azure AI Foundry implementation takes shape.

### 3. Long-term semantic context

The system should be able to search for relevant long-term memories using the normalized meaning of a message. Retrieved memories are additional context, not instructions that override what the user just said. Redis supports the recent conversation window; a separate semantic-memory design will support recall across conversations. The memory provider and its integration with Azure are still to be selected.

### 4. Agent reasoning, replies, and extensible actions

Azure AI Foundry agents will combine the structured message, Redis conversation context, and any relevant long-term memories. The workflow can choose a simple direct reply (such as a greeting), reason through a request, or coordinate a suitable agent or tool. As the system grows, it may also update useful long-term memories, persist application data to MongoDB, or retrieve additional conversation context from Redis.

These are extension points in the intended architecture—not a promise that those actions or a chat workflow are currently wired into the running API.

### 5. Natural response in the user’s language

Before responding, the system will shape the answer for the language or language mix of the original message. For Taglish, that means a natural Taglish response where appropriate—not a stiff, word-for-word translation. The goal is to preserve the answer’s meaning while making it sound clear and conversational. FastAPI will stream generated output directly to the client using `StreamingResponse` over HTTP; the planned design does not add a message queue or use SSE.

## Model and cost approach

The aim is to keep the system useful without requiring an expensive model for every step. Clear structured handoffs, bounded short-term context, and relevant memory retrieval can help avoid sending unnecessary context downstream and make it possible to choose Azure model deployments suited to each task. This is a design goal, not a guarantee of a particular cost or quality level; both will need to be measured as the workflow is implemented.

The language layer should improve understanding, not force every downstream component into a rigid output style. The assistant should still be able to produce smooth, helpful answers.

## Current project status

The repository is an early foundation for the design above. The currently wired FastAPI app exposes a health check and user authentication endpoints. Redis and MongoDB clients are initialized at startup. Azure AI Foundry orchestration, the Taglish understanding pipeline, bounded conversation-history behavior, long-term memory integration, chat endpoints, and streaming responses are not yet connected to the running API. Preparing for the Azure AI-103 exam is part of the learning path for designing the future multi-agent workflow.

Older experimental code lives under `app_orig_copy/`; it should not be mistaken for routes currently served by the main application. A legacy Mem0 repository and its Groq/Cohere/Milvus configuration are still present in the codebase, but they are not initialized by the current API and are not the target agent architecture. The system is text-only at this stage, and voice support remains an open future problem.

## Running the current API

The project uses Python 3.13 and `uv`. The currently wired API expects `MONGO_URI` and `REDIS_URI` at startup. Put local settings in a root `.env` file; configuration is loaded from the process working directory. The legacy Mem0 repository still expects `GROQ_API_KEY`, `COHERE_API_KEY`, `MILVUS_URI`, `MILVUS_TOKEN`, and `MILVUS_COLLECTION_NAME` if that repository is used; these are not required to start the current API and are not the planned Azure configuration.

```bash
uv sync
uv run python main.py
```

The current Docker Compose setup starts the backend with MongoDB and Redis:

```bash
docker compose up --build
```

The API is available at `http://localhost:8000`; its health endpoint is `/health-check`. Authentication routes are mounted under `/api/auth`. Docker Compose does not configure the external services used by the legacy Mem0 repository.

## License

MIT
