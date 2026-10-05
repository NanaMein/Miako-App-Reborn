# Mirai Aiko (Reborn)

**A text-first AI companion designed to understand Taglish, language-switching, and the way people actually talk.**

**Reborn** is an updated, refactored rework of my original Mirai Aiko project—not a brand-new project. It carries forward the earlier project’s foundation while reshaping it around the architecture and goals described here. The idea grew out of my experience abroad; I’ll share the fuller story another time. For now, this README focuses on the product goal and the system I want to build.

## The goal

Mirai Aiko is for people who speak Taglish, use modern Filipino and Gen Z slang, switch languages mid-thought, or otherwise communicate in ways that English-first AI systems can misunderstand. It should follow the user’s meaning and conversational context—even when the language or topic shifts—and return an answer that feels natural in the language and style they used.

The language-understanding layer is meant to identify intent and preserve meaning, not limit what the assistant can say. The response can still be fluent, flexible, and creative; the intermediate structure simply gives the rest of the system a clearer understanding of what the user meant.

The first version is **text-only**. Voice input and output are not part of the current plan.

## Intended architecture

This is the target design, not a claim that every stage is already implemented.

```text
User message
    │
    ▼
Redis short-term conversation window
    │  Keep a bounded, recent history to help resolve context and topic shifts
    ▼
Language understanding and normalization
    │  Detect languages/code-switching and produce validated structured JSON
    ▼
Mem0 semantic-memory retrieval
    │  Search relevant long-term user context using the normalized meaning
    ▼
Reasoning and action selection
    │  Combine the JSON, recent conversation, and retrieved memories
    │  Reply directly, plan a task, or use an available tool
    ▼
Response generation and language/style polish
    │  Return the answer in the language mix and tone of the user's message
    ▼
User
```

### 1. Short-term conversation context — Redis

Before language processing, Redis will keep a small, bounded window of recent conversation. This gives the assistant nearby context for follow-ups and topic changes without treating the entire chat history as permanent memory. The size and expiry policy still need to be defined.

### 2. Language understanding — structured JSON

For non-English and mixed-language input, a language-understanding step will use a language model to interpret the message and produce a structured representation. Depending on the message, that representation may include:

- Detected language or languages and a confidence score.
- A concise English interpretation that preserves the original meaning and context.
- Intent, relevant entities, and task constraints.
- Whether a workflow or tool may be appropriate, with a confidence or uncertainty signal.
- Ambiguities the next step should clarify rather than guess about.

This is an internal handoff format, not the final answer. The intent is to use the model to understand the user—not to depend on scraping or translating web content to interpret ordinary conversation. Structured output should be validated, and uncertainty should remain visible to later steps.

### 3. Long-term semantic context — Mem0

Mem0, backed by a vector store, will search for relevant long-term memories using the normalized meaning of the message. The retrieved memories are additional context, not instructions that override what the user just said. Redis supports the recent conversation window; Mem0 supports semantic recall across conversations.

### 4. Reasoning, replies, and extensible actions

The reasoning step will combine the structured message, Redis conversation context, and any relevant Mem0 results. It can choose a simple direct reply (such as a greeting), reason through a request, or select an available workflow or tool. As the system grows, this layer may also update useful long-term memories, persist application data to MongoDB, call tools through MCP, or retrieve additional conversation context from Redis.

These are extension points in the intended architecture—not a promise that those actions or a chat workflow are currently wired into the running API.

### 5. Natural response in the user’s language

Before responding, the system will shape the answer for the language or language mix of the original message. For Taglish, that means a natural Taglish response where appropriate—not a stiff, word-for-word translation. The goal is to preserve the answer’s meaning while making it sound clear and conversational.

## Model and cost approach

The aim is to keep the system useful without requiring an expensive model for every step. Clear structured handoffs, bounded short-term context, and relevant memory retrieval can help avoid sending unnecessary context downstream and make it possible to choose a suitably capable model for each task. This is a design goal, not a guarantee of a particular cost or quality level; both will need to be measured as the workflow is implemented.

The language layer should improve understanding, not force every downstream component into a rigid output style. The assistant should still be able to produce smooth, helpful answers.

## Current project status

The repository is an early foundation for the design above. The currently wired FastAPI app exposes a health check and user authentication endpoints. Redis and MongoDB clients are initialized at startup, and a Mem0 repository is present for semantic-memory operations. The Taglish understanding pipeline, bounded conversation-history behavior, chat orchestration, tool workflow, and response-language polishing are not yet connected to the running API.

Older experimental code lives under `app_orig_copy/`; it should not be mistaken for routes currently served by the main application. The system is text-only at this stage, and voice support remains an open future problem.

## Running the current API

The project uses Python 3.13 and `uv`. The API expects `MONGO_URI` and `REDIS_URI` at startup. For Mem0, configure `GROQ_API_KEY`, `COHERE_API_KEY`, `MILVUS_URI`, `MILVUS_TOKEN`, and `MILVUS_COLLECTION_NAME` as well. Put local settings in a root `.env` file; configuration is loaded from the process working directory.

```bash
uv sync
uv run python main.py
```

The current Docker Compose setup starts the backend with MongoDB and Redis:

```bash
docker compose up --build
```

The API is available at `http://localhost:8000`; its health endpoint is `/health-check`. Authentication routes are mounted under `/api/auth`. Docker Compose does not configure the external Milvus, Cohere, or Groq services needed to use Mem0.

## License

MIT
