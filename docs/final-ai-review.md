# Final AI Review

This review records how AI-assisted suggestions were evaluated rather than accepted automatically during final-project hardening.

## AI Code Review Mini-Log

| AI review comment | Grade | Decision and evidence |
| --- | --- | --- |
| `Done -> InProgress` was allowed in `VALID_TRANSITIONS`, which conflicted with the forward-only lifecycle. | **Useful** | Verified against `app/business_rules.py`, reproduced with a regression test, then removed the backward transition. |
| The project should be migrated to SQLite/SQLModel because the project description mentioned that architecture. | **Wrong** | Repository inspection showed `app/storage.py` uses an in-memory dictionary and `requirements.txt` contains no SQLModel dependency. The migration was rejected because it would redesign the existing application without need. |
| Add a large lint/type-check/tooling stack to CI to make the release more professional. | **Noise** | The assignment only required credible lightweight CI. The final workflow stays focused on dependency installation, import validation, and pytest so it remains maintainable and relevant. |

## AI Security Mini-Review

| AI security finding | Grade | Decision and evidence |
| --- | --- | --- |
| Strengthen ignore rules for real `.env` files, private keys, logs, caches, and runtime database files. | **Valid** | `.gitignore` and `.dockerignore` were hardened so these artifacts are not accidentally committed or copied into images. |
| `.env.example` itself is a secret and should be removed from the repository. | **False Positive** | The file contains only example development values (`PORT=8000` and `APP_ENV=development`) and no credential, token, or private data. It is intentionally safe to commit. |
| Missing authentication should block this final release. | **Noise** | Authentication is explicitly outside the learning project's scope. Adding it would introduce a new product feature rather than harden the existing Task Tracker. |

## Rejected/Corrected AI Output

### Corrected database assumption

An early AI assumption treated the project as SQLite/SQLModel based on the project description. After inspecting the actual repository, this was corrected: the real storage layer is `app/storage.py`, which uses an in-memory dictionary. The final documentation now describes the implementation that actually exists instead of repeating the incorrect assumption.

### Rejected unverifiable Docker claim

AI-generated release text must not claim Docker was successfully run when no Docker runtime was available. That claim was rejected. The documentation states that Docker configuration was reviewed statically and clearly records the runtime limitation.

### Corrected update validation gap

Evaluator feedback showed that `PATCH {"title": null}` was accepted because `TaskUpdate.title` allowed `None`. The validator was corrected so explicit null is rejected while an omitted title remains valid for partial updates. A regression test also verifies that the previously stored title is preserved after the rejected request.

## Ownership Statement

I understand the Task Tracker request flow from FastAPI request handling through Pydantic validation, business-rule checks, and in-memory storage. I can explain why the project keeps its existing in-memory architecture, how the forward-only status rule works, and how the tests protect these behaviors. I reviewed AI-assisted suggestions rather than accepting them automatically, including correcting the database assumption and rejecting unverifiable claims. I am responsible for the final submitted code and can reproduce the main local verification steps documented in this repository.
