# Graph Report - Mirai_Aiko_Project_Repository  (2026-10-26)

## Corpus Check
- 29 files · ~5,186 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 161 nodes · 247 edges · 23 communities (19 shown, 4 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a2016780`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Settings
- UserLoginService
- main.py
- OpaqueTokenService
- HttpCookieAuthService
- users_service.py
- Mirai Aiko (Reborn)
- main_workflow.py
- SettingsDeveloper
- opencode.json
- dependencies
- graphify.js
- Project guidance
- Mirai-Aiko

## God Nodes (most connected - your core abstractions)
1. `HttpCookieAuthService` - 18 edges
2. `UserLoginService` - 12 edges
3. `OpaqueTokenService` - 10 edges
4. `UserRegisterService` - 9 edges
5. `RedisCacheBaseRepository` - 8 edges
6. `UsersRepository` - 8 edges
7. `PasswordHasherService` - 8 edges
8. `lifespan()` - 8 edges
9. `MongoBase` - 7 edges
10. `UserLoginSchema` - 7 edges

## Surprising Connections (you probably didn't know these)
- `lifespan()` --uses--> `RedisCacheBaseRepository`  [INFERRED]
  main.py → app/repositories/caches.py
- `lifespan()` --uses--> `MongoBase`  [INFERRED]
  main.py → app/repositories/database.py
- `OpaqueTokenService` --uses--> `RedisCacheBaseRepository`  [INFERRED]
  app/services/http_cookie_service.py → app/repositories/caches.py
- `UserLoginService` --uses--> `UserLoginSchema`  [INFERRED]
  app/services/users_service.py → app/schemas/users_schema.py
- `UserRegisterService` --uses--> `UserRegisterSchema`  [INFERRED]
  app/services/users_service.py → app/schemas/users_schema.py

## Import Cycles
- None detected.

## Communities (23 total, 4 thin omitted)

### Community 1 - "UserLoginService"
Cohesion: 0.14
Nodes (8): get_user_login_service(), get_user_register_service(), UsersRepository, PasswordHasherService, UserLoginService, UserRegisterService, AsyncCollection, HttpCookieAuthServiceDepends

### Community 2 - "main.py"
Cohesion: 0.17
Nodes (7): LoguruHandler, RedisCacheBaseRepository, MongoBase, AsyncMongoClient, health_check(), lifespan(), get

### Community 3 - "OpaqueTokenService"
Cohesion: 0.16
Nodes (7): OpaqueTokenService, Request, Response, Returns the sub and token type from the opaque token, if it exists., Deletes the opaque token from the cache., Redis, timedelta

### Community 4 - "HttpCookieAuthService"
Cohesion: 0.24
Nodes (6): get_http_cookie_auth_service(), Request, Response, HttpCookieAuthService, Request, Response

### Community 5 - "users_service.py"
Cohesion: 0.12
Nodes (22): get_user_access_service(), get_user_logout_service(), Request, Response, get_me(), get_sample_user(), login_user(), logout() (+14 more)

### Community 6 - "Mirai Aiko (Reborn)"
Cohesion: 0.20
Nodes (9): Current project status, Future supporting options—not current dependencies or commitments, Intended MAF and Foundry workflow, License, Mirai Aiko (Reborn), Primary foundation: Microsoft Agent Framework and Azure AI Foundry, Product goal and priorities, Running the current API (+1 more)

### Community 7 - "main_workflow.py"
Cohesion: 0.36
Nodes (6): Chat, chat_agent(), BaseModel, post, translator_tool(), LANGUAGES

### Community 9 - "opencode.json"
Cohesion: 0.33
Nodes (5): instructions, plugin, $schema, AGENTS.md, .opencode/plugins/graphify.js

### Community 10 - "dependencies"
Cohesion: 0.50
Nodes (3): @opencode-ai/plugin, dependencies, @opencode-ai/plugin

### Community 12 - "Project guidance"
Cohesion: 0.33
Nodes (5): Architecture and dependency direction, Current API and implementation boundaries, Graphify, Project guidance, Run and configure the current app

## Knowledge Gaps
- **16 isolated node(s):** `$schema`, `AGENTS.md`, `.opencode/plugins/graphify.js`, `@opencode-ai/plugin`, `Mirai-Aiko` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HttpCookieAuthService` connect `HttpCookieAuthService` to `UserLoginService`, `main.py`, `OpaqueTokenService`, `users_service.py`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Why does `OpaqueTokenService` connect `OpaqueTokenService` to `main.py`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `UserLoginService` connect `UserLoginService` to `HttpCookieAuthService`, `users_service.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `HttpCookieAuthService` (e.g. with `UserAccessService` and `UserLoginService`) actually correct?**
  _`HttpCookieAuthService` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `UserLoginService` (e.g. with `UsersRepository` and `UserLoginSchema`) actually correct?**
  _`UserLoginService` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `UserRegisterService` (e.g. with `UsersRepository` and `UserRegisterSchema`) actually correct?**
  _`UserRegisterService` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `AGENTS.md`, `.opencode/plugins/graphify.js` to the rest of the system?**
  _16 weakly-connected nodes found - possible documentation gaps or missing edges._