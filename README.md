# Task Tracker

A FastAPI and vanilla JavaScript Kanban board built through the AI-Assisted
Coding Modules 1-3 and extended with two mid-course features:

- due dates with overdue detection and filtering
- tags with validation, card chips, and filtering

The project intentionally uses in-memory storage. Data resets whenever the
backend restarts.

## Project structure

```text
task-tracker/
├── app/
│   ├── business_rules.py
│   ├── main.py
│   ├── models.py
│   └── storage.py
├── docs/midcourse/
├── frontend/index.html
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Run the backend

Python 3.10 or newer is required.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Linux or macOS

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:

- API health: <http://127.0.0.1:8000/health>
- Swagger documentation: <http://127.0.0.1:8000/docs>

## Open the frontend

Keep the backend terminal running. Open a second terminal in the project folder:

```bash
python -m http.server 5500 --directory frontend
```

Then open <http://127.0.0.1:5500>.

Do not open `frontend/index.html` by double-clicking it. A local HTTP server
gives the page the origin allowed by the backend CORS configuration.

## Run verification and tests

```bash
python -m tests.verify_a
pytest tests/ -v
```

The model verification prints eight `PASS` results. The current test suite
contains 32 tests covering health, CRUD, filtering, validation, status
transitions, due dates, overdue behavior, and tags.

## API summary

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Check API availability |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List and filter tasks |
| `GET` | `/tasks/{task_id}` | Read one task |
| `PATCH` | `/tasks/{task_id}` | Partially update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

`GET /tasks` accepts `status`, `priority`, `overdue`, and `tag` query
parameters. Filters can be combined.

## Scope

This learning project does not include authentication, user accounts,
multi-tenancy, real-time updates, notifications, a production database,
Docker, or deployment.
