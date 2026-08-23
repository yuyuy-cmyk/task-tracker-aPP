# Final AI Review

This review records how AI-assisted suggestions were evaluated rather than accepted automatically during final-project hardening.

## AI Code Review Mini-Log

| AI review comment | Grade | Decision and evidence |
| --- | --- | --- |
| `Done -> InProgress` was allowed in `VALID_TRANSITIONS`, which conflicted with the forward-only lifecycle. | **Useful** | Verified against `app/business_rules.py`, reproduced with a regression test, then removed the backward transition. |
| The project should be migrated to SQLite/SQLModel because the project description mentioned that architecture. | **Wrong** | Repository inspection showed `app/storage.py` uses an in-memory dictionary and `requirements.txt` contains no SQLModel dependency. The migration was rejected because it would redesign the existing application without need. |
| Add a large lint/type-check/tooling stack to CI to make the release more professional. | **Noise** | The assignment calls for a maintainable release, so CI remains focused on reproducible tests plus the required Docker build/run health verification instead of unrelated tooling. |

## AI Security Mini-Review

| AI security finding | Grade | Decision and evidence |
| --- | --- | --- |
| Strengthen ignore rules for real `.env` files, private keys, logs, caches, and runtime database files. | **Valid** | `.gitignore` and `.dockerignore` were hardened so these artifacts are not accidentally committed or copied into images. |
| `.env.example` itself is a secret and should be removed from the repository. | **False Positive** | The file contains only example development values (`PORT=8000` and `APP_ENV=development`) and no credential, token, or private data. It is intentionally safe to commit. |
| Missing authentication should block this final release. | **Noise** | Authentication is outside this learning project's scope. Adding it would introduce a new product feature instead of reviewing the security of the existing Task Tracker. |

## Manual security check

I manually reviewed the tracked repository structure and the security-sensitive configuration files before final submission.

- Confirmed that no real `.env` file is tracked; only `.env.example` is present.
- Confirmed `.env.example` contains only `PORT=8000` and `APP_ENV=development`, not a token, password, API key, or credential.
- Reviewed `.gitignore` and `.dockerignore` to ensure real environment files, private keys, logs, caches, virtual environments, runtime database files, editor files, and generated output are excluded.
- Reviewed the application code for hard-coded credentials or customer/personal data and found none required by the application.
- Confirmed the project does not claim authentication as a security control because authentication is explicitly outside the application scope.
- Confirmed CORS remains restricted to the documented local frontend origins rather than being changed as part of the final review.

## Three AI usage rules

1. **Inspect before changing.** Read the real repository, tests, dependencies, and requirements before accepting an architectural assumption from AI.
2. **Verify every meaningful change.** AI-generated code must be checked with deterministic tests and, where relevant, a manual or runtime verification step before it is accepted.
3. **Reject unsafe or unverifiable output.** Never commit secrets, never fabricate test or Docker results, and reject AI suggestions that add unnecessary scope or cannot be explained and maintained.

## AGENTS.md guardrails

`AGENTS.md` is the repository-level instruction set for AI-assisted work. The final review checked the changes against its guardrails rather than treating AI output as automatically correct.

The important guardrails used in this release are:

- **Preserve the current architecture:** keep the FastAPI/Pydantic backend, vanilla frontend, and in-memory storage unless a requirement explicitly calls for a change.
- **Prefer small, readable changes:** do not replace working code with a large rewrite just because an AI agent suggests one.
- **Protect business rules:** titles must be valid, task status follows `ToDo -> InProgress -> Done`, completed tasks do not move backward, and request validation must not be weakened.
- **Validate changes:** add or update tests, run pytest, verify the app imports, and update documentation when behavior or tooling changes.
- **Protect repository security:** never commit real secrets, tokens, credentials, private keys, personal/customer data, production logs, or real `.env` files.
- **Do not fake evidence:** never state that a command, test, or container check passed unless it actually executed successfully.

These guardrails directly caused several final decisions: the SQLite/SQLModel rewrite suggestion was rejected, the null-title bug received a focused regression test, and Docker success is documented only after an actual image build, container run, and `/health` check.

## Rejected/Corrected AI Output

### Corrected database assumption

An early AI assumption treated the project as SQLite/SQLModel based on the project description. After inspecting the actual repository, this was corrected: the real storage layer is `app/storage.py`, which uses an in-memory dictionary. The final documentation describes the implementation that actually exists instead of repeating the incorrect assumption.

### Rejected unverifiable Docker claim

An earlier release draft correctly refused to claim Docker worked because no Docker runtime had actually executed it. After evaluator feedback, Docker verification was changed from static review to an executable build/run check: the image must build, the container must start, and `/health` must return HTTP 200. The concrete run evidence belongs in `docs/release-evidence.md` and is recorded only from an actually completed run.

### Corrected update validation gap

Evaluator feedback showed that `PATCH {"title": null}` was accepted because `TaskUpdate.title` allowed `None`. The validator was corrected so explicit null is rejected while an omitted title remains valid for partial updates. A regression test also verifies that the previously stored title is preserved after the rejected request.

## Ownership Statement

I understand the Task Tracker request flow from FastAPI request handling through Pydantic validation, business-rule checks, and in-memory storage. I can explain why the project keeps its existing architecture, how the forward-only status rule and null-title validation work, and how the tests protect those behaviors. I use AI as an assistant but review its suggestions against `AGENTS.md`, deterministic tests, security checks, and actual runtime evidence before accepting them. I am responsible for the final submitted code and can reproduce the main verification steps documented in this repository.
