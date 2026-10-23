# Graph Report - Mirai_Aiko_Project_Repository  (2026-10-22)

## Corpus Check
- 27 files · ~4,946 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 161 nodes · 243 edges · 22 communities (18 shown, 4 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8db06a96`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Settings
- users_service.py
- main.py
- OpaqueTokenService
- HttpCookieAuthService
- auth_router.py
- Mirai Aiko (Reborn)
- users_dependency.py
- AgentMemoryRepository
- opencode.json
- dependencies
- graphify.js
- AGENTS.md
- Mirai-Aiko

## God Nodes (most connected - your core abstractions)
1. `HttpCookieAuthService` - 18 edges
2. `Settings` - 12 edges
3. `UserLoginService` - 12 edges
4. `OpaqueTokenService` - 10 edges
5. `UserRegisterService` - 9 edges
6. `AgentMemoryRepository` - 8 edges
7. `RedisCacheBaseRepository` - 8 edges
8. `UsersRepository` - 8 edges
9. `PasswordHasherService` - 8 edges
10. `lifespan()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `lifespan()` --uses--> `RedisCacheBaseRepository`  [INFERRED]
  main.py → app/repositories/caches.py
- `lifespan()` --uses--> `MongoBase`  [INFERRED]
  main.py → app/repositories/database.py
- `get_user_register_service()` --calls--> `UserRegisterService`  [EXTRACTED]
  app/dependencies/users_dependency.py → app/services/users_service.py
- `OpaqueTokenService` --uses--> `RedisCacheBaseRepository`  [INFERRED]
  app/services/http_cookie_service.py → app/repositories/caches.py
- `register_user()` --uses--> `UserRegisterSchema`  [INFERRED]
  app/routers/auth_router.py → app/schemas/users_schema.py

## Import Cycles
- None detected.

## Communities (22 total, 4 thin omitted)

### Community 0 - "Settings"
Cohesion: 0.12
Nodes (3): Settings, LoguruHandler, ZoneInfo

### Community 1 - "users_service.py"
Cohesion: 0.19
Nodes (7): UsersRepository, UserLoginSchema, UserRegisterSchema, PasswordHasherService, UserLoginService, UserRegisterService, BaseModel

### Community 2 - "main.py"
Cohesion: 0.19
Nodes (8): RedisCacheBaseRepository, MongoBase, AsyncCollection, AsyncMongoClient, FastAPI, health_check(), lifespan(), get

### Community 3 - "OpaqueTokenService"
Cohesion: 0.16
Nodes (7): OpaqueTokenService, Request, Response, Returns the sub and token type from the opaque token, if it exists., Deletes the opaque token from the cache., Redis, timedelta

### Community 4 - "HttpCookieAuthService"
Cohesion: 0.24
Nodes (6): get_http_cookie_auth_service(), Request, Response, HttpCookieAuthService, Request, Response

### Community 5 - "auth_router.py"
Cohesion: 0.21
Nodes (12): get_me(), get_sample_user(), login_user(), logout(), get, random_user(), register_user(), post (+4 more)

### Community 6 - "Mirai Aiko (Reborn)"
Cohesion: 0.15
Nodes (12): 1. API and short-term conversation context — FastAPI and Redis, 2. Language understanding and orchestration — Azure AI Foundry, 3. Long-term semantic context, 4. Agent reasoning, replies, and extensible actions, 5. Natural response in the user’s language, Current project status, Intended architecture, License (+4 more)

### Community 7 - "users_dependency.py"
Cohesion: 0.23
Nodes (9): get_user_access_service(), get_user_login_service(), get_user_logout_service(), get_user_register_service(), Request, Response, UserAccessService, UserLogoutService (+1 more)

### Community 9 - "opencode.json"
Cohesion: 0.33
Nodes (5): instructions, plugin, $schema, AGENTS.md, .opencode/plugins/graphify.js

### Community 10 - "dependencies"
Cohesion: 0.50
Nodes (3): @opencode-ai/plugin, dependencies, @opencode-ai/plugin

## Knowledge Gaps
- **16 isolated node(s):** `$schema`, `AGENTS.md`, `.opencode/plugins/graphify.js`, `@opencode-ai/plugin`, `Mirai-Aiko` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HttpCookieAuthService` connect `HttpCookieAuthService` to `users_service.py`, `main.py`, `OpaqueTokenService`, `users_dependency.py`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._
- **Why does `OpaqueTokenService` connect `OpaqueTokenService` to `main.py`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `HttpCookieAuthService` (e.g. with `UserAccessService` and `UserLoginService`) actually correct?**
  _`HttpCookieAuthService` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `UserLoginService` (e.g. with `UsersRepository` and `UserLoginSchema`) actually correct?**
  _`UserLoginService` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `UserRegisterService` (e.g. with `UsersRepository` and `UserRegisterSchema`) actually correct?**
  _`UserRegisterService` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `AGENTS.md`, `.opencode/plugins/graphify.js` to the rest of the system?**
  _16 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Settings` be split into smaller, more focused modules?**
  _Cohesion score 0.11578947368421053 - nodes in this community are weakly interconnected._