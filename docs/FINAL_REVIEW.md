# Final Review and Evaluation Study Guide

## What changed for the final release

The final branch hardens the existing Task Tracker without adding unrelated product features. It preserves the FastAPI backend, Pydantic models, in-memory storage, vanilla frontend, due dates, tags, filters, and CRUD API.

A real correctness issue was fixed: completed tasks could move from `Done` back to `InProgress`. The valid lifecycle is now forward-only: `ToDo -> InProgress -> Done`.

Release engineering was added through GitHub Actions CI, Dockerfiles for backend and frontend, Compose, stronger ignore rules, `AGENTS.md`, and final engineering documentation.

## Architecture to explain

- `app/main.py`: HTTP routes, CORS, filters, HTTP errors.
- `app/models.py`: Pydantic validation and task schema.
- `app/business_rules.py`: allowed status transitions.
- `app/storage.py`: in-memory task dictionary and CRUD helpers.
- `frontend/index.html`: static browser interface.
- `tests/`: API regression tests using FastAPI `TestClient`.

The backend does not use SQLite/SQLModel in the current code. Data disappears when the backend restarts. This was deliberately preserved to avoid an unnecessary redesign.

## Backend request flow

A request enters FastAPI, is validated by Pydantic, passes route/business-rule checks, calls the storage helper, and returns a validated JSON response. Invalid input normally returns `422`; missing task IDs return `404`.

## Frontend flow

The static JavaScript UI sends HTTP requests to the API on port 8000. For local development it is served on port 5500, which matches the backend CORS configuration.

## Tests to understand

Tests reset in-memory storage before and after each test so tests are isolated. They cover health, CRUD, validation, filters, status rules, due dates/overdue behavior, and tags. The final release adds a regression specifically for `Done -> InProgress`.

During final-release work, a targeted executable verification first failed on that rollback rule, then passed `9 passed in 0.10s` after the fix. The FastAPI import check also succeeded.

## CI to explain

`.github/workflows/ci.yml` runs on relevant pushes and pull requests. It checks out the repository, installs Python 3.11, installs `requirements.txt`, imports the FastAPI app, and runs pytest. A failing test causes CI to fail.

## Docker to explain

- Root `Dockerfile`: Python 3.11 slim backend image running Uvicorn on port 8000.
- `frontend/Dockerfile`: Nginx serves the static frontend.
- `compose.yaml`: runs both services together, exposing frontend port 5500 and backend port 8000.
- `.dockerignore`: prevents secrets, caches, logs, runtime databases, and unrelated files from entering the backend build context.

## Security review to explain

The repository was reviewed for real `.env` files, secrets, tokens, credentials, logs, database artifacts, and personal/customer data. `.env.example` contains only safe development placeholders. Searches for `password` and `token` returned no repository matches during review. Ignore rules were strengthened.

## Important engineering decisions

1. Preserve in-memory storage instead of introducing a new database.
2. Preserve the vanilla frontend instead of adding a framework.
3. Fix only the demonstrated status-transition bug.
4. Keep CI and Docker simple and explainable.
5. Do not claim Docker or CI execution unless the environment actually ran it.

## What Codex/AI changed

AI assistance inspected the repository and assignment, identified missing final-release artifacts, reproduced the status-rule bug with a regression test, prepared the fix, created CI/Docker configuration, strengthened ignore rules, and drafted repository-specific documentation. Human ownership still requires understanding and being able to explain every final change.

## Before evaluation

Be ready to explain why `Done` is terminal, why test storage is reset, why the app uses in-memory persistence, what each Docker service does, what CI checks, why `.env.example` is safe to commit, and the difference between verification that was actually executed and configuration that was only statically reviewed.
