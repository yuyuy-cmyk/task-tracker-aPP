# AGENTS.md

## Project purpose

This repository contains an AUB AI-Assisted Coding course Task Tracker. It is a small FastAPI backend with an in-memory task store and a vanilla HTML/CSS/JavaScript frontend. The goal of this branch is maintainability and release readiness, not feature expansion.

## Architecture

- `app/main.py`: FastAPI application, routes, CORS, filtering, HTTP errors.
- `app/models.py`: Pydantic request/response models, enums, validation, due-date and tag behavior.
- `app/business_rules.py`: allowed task status transitions.
- `app/storage.py`: in-memory dictionary persistence. Data intentionally resets on restart.
- `frontend/index.html`: static browser UI calling the backend API.
- `tests/`: pytest API tests and fixtures.
- `docs/`: engineering evidence and course documentation.

## Run locally

```bash
python -m venv .venv
# activate the environment
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
python -m http.server 5500 --directory frontend
```

API docs are at `http://127.0.0.1:8000/docs` and the frontend is at `http://127.0.0.1:5500`.

## Run tests

```bash
python -m pytest tests/ -q
python -m tests.verify_a
```

Before finishing a change, at minimum import the application and run pytest.

## Business rules

- Title is required, trimmed, non-blank, and limited to 200 characters.
- Status values are `ToDo`, `InProgress`, and `Done`.
- Priority values are `Low`, `Medium`, and `High`.
- Allowed status progression is `ToDo -> InProgress -> Done`.
- A completed task must not move backward.
- A task is overdue only when it has a past due date and is not `Done`.
- Tags are trimmed, case-insensitively de-duplicated, limited to 10 tags, and limited to 30 characters each.
- Request models reject unknown fields.

## Change rules

- Prefer small, readable changes over rewrites.
- Preserve current routes and response shapes unless a documented requirement requires a breaking change.
- Do not replace in-memory storage with a database unless the assignment explicitly requires it.
- Do not add authentication, accounts, notifications, multi-tenancy, real-time features, or deployment systems without justification.
- Keep backend and frontend assumptions synchronized, especially API URL and CORS ports.

## Validation expectations

For significant changes:

1. Add or update tests for success and failure behavior.
2. Run `python -m pytest tests/ -q`.
3. Verify `python -c "from app.main import app"` succeeds.
4. Check documentation when behavior or commands change.
5. Review the diff for temporary files or unrelated edits.

Never claim a command passed unless it was actually run.

## Security expectations

- Never commit real `.env` files, secrets, tokens, private keys, credentials, customer data, personal data, or production logs.
- `.env.example` must contain only fake/example values.
- Keep runtime database files, logs, caches, virtual environments, and editor files ignored.
- Do not weaken validation or CORS behavior without a documented reason.

## Documentation expectations

Update `README.md` and relevant files in `docs/` when changing architecture, workflow, behavior, testing, Docker, CI, or security assumptions. Record what changed, why, and how it was verified.
