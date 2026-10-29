# Project guidance

## Run and configure the current app

- Run development commands from the repository root: `uv sync`, then `uv run python main.py`.
- `main.py` initializes Redis and MongoDB in its lifespan. The current app needs `REDIS_URI` and `MONGO_URI` for that startup.
- `app/core/config.py` calls `load_dotenv()` at import time, loading `.env` from the process working directory. `AZURE_PROJECT_ENDPOINT` is also required for startup: `main.py` imports `app/workflows/main_workflow.py`, which constructs the Foundry client at module import and reads this setting then.
- Keep the current configuration separation: shared application settings are in `Settings`/`settings`; Azure test settings remain in `SettingsDeveloper`/`settings_dev`. Do not merge or relocate those settings as part of unrelated work.
- Chat requests use `DefaultAzureCredential` and the Azure Translator settings (`AZURE_TRANSLATOR_ENDPOINT` and `AZURE_TRANSLATOR_KEY`). These are needed for the current chat workflow; Translator settings are not the same as the project endpoint needed during import.
- `docker-compose.yaml` maps the backend to `127.0.0.1:8000` and starts MongoDB and Redis without exposing their ports. It currently passes only `MONGO_URI` and `REDIS_URI` to the backend, not `AZURE_PROJECT_ENDPOINT`; account for that before expecting the containerized app to start. Do not commit Azure credentials or other secrets.

## Current API and implementation boundaries

- `main.py` mounts `app/routers/auth_router.py` under `/api/auth`, mounts `chat_router` from `app/workflows/main_workflow.py` under `/api`, and exposes `/health-check`.
- The current routes include `GET /api/auth/sample-user-for-testing`, `POST /api/auth/register-user`, `POST /api/auth/login-user`, `GET /api/auth/me`, `GET /api/auth/logout`, and `POST /api/chat`.
- Auth cookies are named `access` and `refresh` and use opaque Redis tokens. `IS_DEPLOYED_FOR_PRODUCTION=true` makes cookies secure; SameSite is `lax` for access and `strict` for refresh. Token TTLs are 7 minutes and 7 days respectively. `/api/auth/me` may use refresh-token handling and re-issue cookies when the access token cannot be used.
- The chat workflow is intentionally a small test implementation: one Microsoft Agent Framework `Agent` uses `FoundryChatClient` with `DeepSeek-V4-Flash`; the handler translates Filipino input to English, runs the agent, translates the response back to Filipino, and returns a normal JSON `Chat` response.
- The translation helper in `app/workflows/tools.py` is called directly; it is not registered as an agent tool. The current chat handler has no cookie-auth dependency. Treat `/api/chat` as an experimental, unauthenticated prototype—not as the completed Taglish pipeline or a production-ready authenticated chat API.
- Keep chat output as ordinary REST/JSON for now. Do not introduce streaming, SSE, a message broker, conversation history, semantic memory, extra agent roles, or automation unless the user requests that work. Streaming is deliberately deferred while the MAF workflow is being learned and designed.
- Redis currently stores authentication tokens, not chat history. MongoDB currently supports user persistence, not agent memory. There is no current long-term semantic-memory or RAG integration.
- Grow the workflow gradually within `app/`, isolating work into appropriate workflows, services, and repositories when useful. Do not over-refactor the current simple test path in anticipation of hypothetical features.
- The current tree does not contain `app_orig_copy/`, `app/workflows/agent_pipeline.py`, or the previously described legacy Mem0/Groq/Cohere/Milvus repository. Use the current source tree as authoritative; do not refer to those removed paths as implemented project components.

## Architecture and dependency direction

- Microsoft Agent Framework (MAF) is the primary agent-framework direction. Azure AI Foundry is the current main platform focus, but Azure is not an irrevocable provider commitment; keep future provider choices open where practical.
- Near-term priorities are: (1) Taglish/code-switching/slang understanding and conversation context, with evaluations; (2) cost-effective responses that meet measured quality goals; and only then (3) tools and automation such as n8n, after the first two priorities have solid implementations and pass evaluations.
- LlamaIndex, Mem0, CrewAI, LangChain, and n8n are possible future supporting options, not current installed components or requirements. Do not add them speculatively; introduce an integration only for a concrete use case.
- `pyproject.toml` is the source for declared project dependencies. Current source directly imports `azure.identity`, `requests`, and `dotenv`, which are not listed there as direct dependencies. If dependency maintenance becomes part of a task, verify the resolved environment and add only the minimal direct dependencies actually needed; do not use that as a reason to add unrelated AI frameworks.

## Graphify

This project has a knowledge graph at `graphify-out/` with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "..."` when `graphify-out/graph.json` exists. Use `graphify path "A" "B"` for relationships and `graphify explain "concept"` for focused concepts. These return a scoped subgraph, usually much smaller than `GRAPH_REPORT.md` or raw grep output.
- Dirty graphify-out files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If `graphify-out/wiki/index.md` exists, use it for broad navigation instead of raw source browsing.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when query/path/explain do not surface enough context.
- After edits, run `graphify update .` to keep the graph current (AST-only, no API cost).
