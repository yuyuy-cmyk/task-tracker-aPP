# Task Tracker

A teammate-maintainable final release of the AUB AI-Assisted Coding Task Tracker. The project combines a FastAPI JSON API with a build-free vanilla HTML/CSS/JavaScript frontend.

Existing functionality includes task creation, viewing, filtering, partial updates, deletion, status and priority, assignees, due dates with overdue detection, and validated tags.

## Architecture

- **Backend:** FastAPI + Pydantic
- **Storage:** in-memory Python dictionary in `app/storage.py`
- **Frontend:** static `frontend/index.html`
- **Tests:** pytest + FastAPI `TestClient`
- **CI:** GitHub Actions
- **Containers:** Docker + Compose

The project intentionally keeps in-memory storage. Data resets whenever the backend process or container restarts.

## Repository structure

```text
task-tracker-aPP/
├── .github/workflows/ci.yml
├── app/
│   ├── business_rules.py
│   ├── main.py
│   ├── models.py
│   └── storage.py
├── docs/
│   ├── AI_ASSISTED_DEVELOPMENT.md
│   ├── ARCHITECTURE.md
│   ├── CODE_REVIEW.md
│   ├── FINAL_REVIEW.md
│   ├── SECURITY_REVIEW.md
│   ├── TESTING.md
│   └── midcourse/
├── frontend/
│   ├── Dockerfile
│   └── index.html
├── tests/
├── .dockerignore
├── .env.example
├── .gitignore
├── AGENTS.md
├── compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Prerequisites

- Python 3.10 or newer; CI uses Python 3.11
- `pip`
- Optional: Docker with Docker Compose

## Local setup

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No real secret is required. `.env.example` contains development-only example values. If you create a local `.env`, never commit it.

## Start the backend

```bash
uvicorn app.main:app --reload --port 8000
```

Useful URLs:

- Health: `http://127.0.0.1:8000/health`
- Swagger/OpenAPI UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Start the frontend

Keep the backend running, then use another terminal:

```bash
python -m http.server 5500 --directory frontend
```

Open `http://127.0.0.1:5500`.

Serving the frontend over HTTP is preferred to double-clicking the file because port 5500 is explicitly allowed by the backend CORS configuration.

## API summary

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List/filter tasks |
| `GET` | `/tasks/{task_id}` | Read one task |
| `PATCH` | `/tasks/{task_id}` | Partially update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

`GET /tasks` supports the `status`, `priority`, `overdue`, and `tag` query parameters. Filters can be combined.

## Important business rules

- Titles are trimmed and cannot be blank.
- Status values are `ToDo`, `InProgress`, and `Done`.
- Priority values are `Low`, `Medium`, and `High`.
- Valid status progression is `ToDo -> InProgress -> Done`.
- Completed tasks cannot move backward.
- A task is overdue only when its due date is in the past and its status is not `Done`.
- Tags are validated, trimmed, and case-insensitively de-duplicated.
- Unknown request fields are rejected.

## Run tests

```bash
python -m pytest tests/ -q
python -m tests.verify_a
```

For a quick import check:

```bash
python -c "from app.main import app; print(app.title, app.version)"
```

The final release adds regression coverage for the completed-task rollback rule. See `docs/TESTING.md` for verification evidence.

## Docker

Build and run both services:

```bash
docker compose up --build
```

Then open:

- Frontend: `http://127.0.0.1:5500`
- Backend: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

Stop the services with:

```bash
docker compose down
```

The backend image uses Python 3.11 slim. The frontend image uses Nginx to serve the existing static page.

## CI

`.github/workflows/ci.yml` runs on relevant pushes and pull requests. It:

1. checks out the repository;
2. sets up Python 3.11;
3. installs `requirements.txt`;
4. imports the FastAPI application;
5. runs pytest.

Any failing command makes the workflow fail.

## Development workflow

1. Work from an appropriate feature/final branch.
2. Keep changes small and consistent with the current architecture.
3. Add or update tests for behavior changes.
4. Run the test suite and application import check.
5. Update documentation when commands, behavior, architecture, CI, Docker, or security assumptions change.
6. Review the complete diff and git status before committing.

AI coding agents should also follow `AGENTS.md`.

## Security and repository hygiene

Never commit real `.env` files, credentials, API keys, tokens, private keys, customer/personal data, production logs, runtime databases, or generated caches. The repository includes hardened `.gitignore` and `.dockerignore` rules. See `docs/SECURITY_REVIEW.md`.

## Scope and constraints

This is a learning project. It intentionally does not add authentication, accounts, multi-tenancy, real-time updates, notifications, a production database, or production deployment infrastructure. The final release focuses on verification, maintainability, documentation, CI, Docker, and security hygiene rather than new product features.

## Troubleshooting

- **Frontend cannot reach backend:** make sure Uvicorn is running on port 8000 and serve the frontend on port 5500.
- **Import errors:** activate the virtual environment and reinstall `requirements.txt`.
- **Tests affect each other:** use the existing pytest fixtures, which reset the in-memory storage around each test.
- **Data disappeared after restart:** this is expected because persistence is in-memory.

## Engineering evidence

See the `docs/` directory for architecture, testing, AI-assisted development, code review, security review, and the final evaluation study guide.
