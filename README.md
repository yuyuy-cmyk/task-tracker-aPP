# Task Tracker

A teammate-maintainable final release of the AUB AI-Assisted Coding Task Tracker. The project combines a FastAPI JSON API with a build-free vanilla HTML/CSS/JavaScript frontend.

Existing functionality includes task creation, viewing, filtering, partial updates, deletion, status and priority, assignees, due dates with overdue detection, and validated tags.

## Final Project

This `final-project` branch is the end-of-course release. It hardens and verifies the existing Task Tracker without replacing the application's architecture or adding unrelated product features.

Required final-project evidence is documented under the exact course filenames:

- [`docs/release-evidence.md`](docs/release-evidence.md) — automated tests, **Manual Check**, actual Docker build/run `/health` evidence, CI evidence, and the release checklist.
- [`docs/final-ai-review.md`](docs/final-ai-review.md) — **AI Code Review Mini-Log**, **AI Security Mini-Review**, **Manual security check**, **Three AI usage rules**, **AGENTS.md guardrails**, **Rejected/Corrected AI Output**, and the 3–5 sentence **Ownership Statement**.
- [`docs/ai-playbook.md`](docs/ai-playbook.md) — **When I reach for AI first**, **When I do not reach for AI first**, **My non-negotiables**, **My review rules**, **What I am still figuring out**, and the **Decision Card**.

A final validation correction also rejects an explicit `null` title during task updates. `PATCH /tasks/{id}` with `{"title": null}` returns HTTP 422 and leaves the stored title unchanged, while omitting `title` remains valid for normal partial updates. The regression case is covered in `tests/test_tasks.py`.

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
│   ├── release-evidence.md
│   ├── final-ai-review.md
│   ├── ai-playbook.md
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

- Titles are trimmed and cannot be blank or explicitly set to null.
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

The final release includes regression coverage for completed-task rollback and explicit null-title updates. See `docs/release-evidence.md` for current verification evidence.

## Docker

### Backend image verification

Build the backend image, run it, and check `/health`:

```bash
docker build -t task-tracker-final .
docker run -d --name task-tracker-final -p 8000:8000 task-tracker-final
curl -i http://127.0.0.1:8000/health
docker rm -f task-tracker-final
```

This exact build/run/health-check flow has been executed successfully in a clean Ubuntu Docker runtime. The observed `/health` response was HTTP 200. See `docs/release-evidence.md` for the recorded image/container IDs and response body.

### Run both services with Compose

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

`.github/workflows/ci.yml` runs on relevant pushes and pull requests with two jobs:

1. **test** — checks out the repository, sets up Python 3.11, installs `requirements.txt`, imports the FastAPI application, and runs the full pytest suite.
2. **docker-verification** — builds the backend image, starts the container, polls `GET /health` until it receives HTTP 200, displays the running container, and cleans it up.

Workflow run **32636518962** completed successfully with both jobs passing; the test job reported **34 passed** and the Docker job received **HTTP 200** from the running container's `/health` endpoint. Detailed evidence is in `docs/release-evidence.md`.

## Development workflow

1. Work from an appropriate feature/final branch.
2. Keep changes small and consistent with the current architecture.
3. Add or update tests for behavior changes.
4. Run the test suite and application import check.
5. Update documentation when commands, behavior, architecture, CI, Docker, or security assumptions change.
6. Review the complete diff and git status before committing.

AI coding agents should also follow `AGENTS.md` and `docs/ai-playbook.md`.

## Security and repository hygiene

Never commit real `.env` files, credentials, API keys, tokens, private keys, customer/personal data, production logs, runtime databases, or generated caches. The repository includes hardened `.gitignore` and `.dockerignore` rules. The required manual security check and AI security review are in `docs/final-ai-review.md`.

## Scope and constraints

This is a learning project. It intentionally does not add authentication, accounts, multi-tenancy, real-time updates, notifications, a production database, or production deployment infrastructure. The final release focuses on verification, maintainability, documentation, CI, Docker, and security hygiene rather than new product features.

## Troubleshooting

- **Frontend cannot reach backend:** make sure Uvicorn is running on port 8000 and serve the frontend on port 5500.
- **Import errors:** activate the virtual environment and reinstall `requirements.txt`.
- **Tests affect each other:** use the existing pytest fixtures, which reset the in-memory storage around each test.
- **Data disappeared after restart:** this is expected because persistence is in-memory.

## Engineering evidence

Start with the three exact required final-project documents: `docs/release-evidence.md`, `docs/final-ai-review.md`, and `docs/ai-playbook.md`. The other documents in `docs/` provide additional architecture, testing, AI-assisted development, code review, security review, and evaluation notes.
