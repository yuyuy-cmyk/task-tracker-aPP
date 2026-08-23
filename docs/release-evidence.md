# Release Evidence

This document records final verification evidence for the AUB AI-Assisted Coding Task Tracker on the `final-project` branch.

## Final Release Scope

The release keeps the existing FastAPI + Pydantic backend, in-memory storage, and vanilla HTML/CSS/JavaScript frontend. Final-project work focuses on maintainability, testing, CI, Docker support, documentation, security hygiene, and correction of verified defects rather than unrelated feature expansion.

The final branch includes:

- `README.md` with a `Final Project` section
- `AGENTS.md`
- `.github/workflows/ci.yml`
- `Dockerfile`, `frontend/Dockerfile`, `compose.yaml`, and `.dockerignore`
- `app/`, `frontend/`, and `tests/`
- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

## Automated Test Evidence

The test suite covers health, create/read/list/update/delete behavior, validation failures, filters, status transitions, due dates, overdue behavior, and tags.

A regression test covers the evaluator-reported case where an explicit null title was previously accepted during a task update:

```python
def test_patch_null_title_returns_422_and_preserves_title(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"title": None})
    assert response.status_code == 422
    stored = client.get(f"/tasks/{task_id}")
    assert stored.status_code == 200
    assert stored.json()["title"] == "Test task"
```

The CI test job executed:

```bash
python -m pytest tests/ -q
```

Observed result on GitHub Actions run **32636518962** (CI run **#25**, 23 August 2026):

```text
..................................                                       [100%]
34 passed, 1 warning in 0.18s
```

The warning was a Starlette/TestClient deprecation warning and did not affect the test result.

The null-title fix is in `app/models.py`: when `title` is explicitly supplied as `null` in `TaskUpdate`, Pydantic raises `Title must not be null`. Omitting `title` remains valid for a normal partial update.

## Manual Check

A direct API check was performed with FastAPI `TestClient` after the null-title fix.

Steps:

1. Create a task named `Manual check task`.
2. Patch the task with `{"title": null}`.
3. Read the task again.
4. Check `/health`.

Observed output:

```text
create_status= 201
null_title_update_status= 422
stored_title= Manual check task
health_status= 200 ok
```

This confirms that an explicit null title is rejected and the stored task remains unchanged.

## CI Evidence

`.github/workflows/ci.yml` now has two executable jobs:

1. `test` — sets up Python 3.11, installs dependencies, imports the FastAPI application, and runs the full pytest suite.
2. `docker-verification` — builds the backend Docker image, starts a real container, calls `/health`, requires HTTP 200, displays the running container, and removes it afterward.

A clean GitHub-hosted **Ubuntu 24.04** runner executed both jobs in workflow run **32636518962**. The workflow completed with conclusion **success**. Both the `test` and `docker-verification` jobs completed successfully.

## Docker Build and Run Evidence

Docker verification is no longer static-only. The backend image was actually built and run in a clean Docker-enabled Ubuntu environment using the same commands a developer runs locally.

### 1. Build the image

Executed command:

```bash
docker build -t task-tracker-final .
```

Result: **success**.

The build produced image:

```text
sha256:3c080df11fddd62757a0e6d47c2291ff962f7e7074a4f2d417905ef09f930923
```

### 2. Run the container

Executed command:

```bash
docker run -d --name task-tracker-final -p 8000:8000 task-tracker-final
```

Result: **success**.

Container ID:

```text
b64ec9a154873f05015de30ba8428570b960dfac9665024debbe21b66cc8e74f
```

### 3. Verify `/health` returns HTTP 200

Executed against the running container:

```bash
curl http://127.0.0.1:8000/health
```

The first attempt occurred while Uvicorn was still starting; the retry succeeded. Observed result:

```text
HTTP status: 200
{"status":"ok","timestamp":"2026-08-23T11:26:10.649952+00:00"}
```

This directly verifies the required behavior: the built image starts successfully and the running container responds to `/health` with **HTTP 200**.

### 4. Confirm the container is running

`docker ps` showed:

```text
IMAGE                STATUS        PORTS                                         NAMES
task-tracker-final   Up 1 second   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   task-tracker-final
```

### 5. Cleanup

Executed:

```bash
docker rm -f task-tracker-final
```

Result: **success**.

### Reproducible local commands

A developer with Docker installed can reproduce the same verification locally with:

```bash
docker build -t task-tracker-final .
docker run -d --name task-tracker-final -p 8000:8000 task-tracker-final
curl -i http://127.0.0.1:8000/health
docker rm -f task-tracker-final
```

## Release Checklist

- README contains a `Final Project` section.
- Exact required documentation files exist.
- `docs/final-ai-review.md` contains the AI code review mini-log, AI security mini-review, `Manual security check`, `Three AI usage rules`, `AGENTS.md guardrails`, `Rejected/Corrected AI Output`, and the Ownership Statement.
- `docs/ai-playbook.md` contains `When I reach for AI first`, `When I do not reach for AI first`, `My non-negotiables`, `My review rules`, `What I am still figuring out`, and the Decision Card.
- Null-title updates are rejected with HTTP 422.
- Regression coverage verifies the stored title is preserved after rejection.
- Full CI test suite passes: **34 tests**.
- Docker image build succeeds.
- Docker container starts successfully.
- The running Docker container responds to `/health` with **HTTP 200**.
- Forward-only task status progression remains enforced.
- No real secrets are introduced by these changes.
