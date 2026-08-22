# Release Evidence

This document records the final verification evidence for the AUB AI-Assisted Coding Task Tracker final project on the `final-project` branch.

## Final Release Scope

The release keeps the existing FastAPI + Pydantic backend, in-memory storage, and vanilla HTML/CSS/JavaScript frontend. The final-project work focuses on maintainability, tests, CI, Docker support, documentation, security hygiene, and correcting verified defects rather than adding unrelated product features.

The final branch includes:

- `README.md` with a Final Project section
- `AGENTS.md`
- `.github/workflows/ci.yml`
- `Dockerfile`, `frontend/Dockerfile`, `compose.yaml`, and `.dockerignore`
- `app/`, `frontend/`, and `tests/`
- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

## Automated Test Evidence

The test suite covers health, create/read/list/update/delete behavior, validation failures, filters, status transitions, due dates, overdue behavior, and tags.

A regression test was added for the evaluator-reported case where an explicit null title was previously accepted during a task update:

```python
def test_patch_null_title_returns_422_and_preserves_title(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"title": None})
    assert response.status_code == 422
    stored = client.get(f"/tasks/{task_id}")
    assert stored.status_code == 200
    assert stored.json()["title"] == "Test task"
```

Verification command:

```bash
python -m pytest tests/test_tasks.py -q
```

Observed result after the null-title fix:

```text
..................................                                       [100%]
34 passed in 0.19s
```

The fix is in `app/models.py`: when `title` is explicitly supplied as `null` in `TaskUpdate`, Pydantic now raises `Title must not be null`. Omitting `title` is still valid for partial updates.

## Manual Check

A direct API check was performed with FastAPI `TestClient` after the fix.

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

`.github/workflows/ci.yml` is configured to run on relevant pushes and pull requests. It checks out the repository, sets up Python 3.11, installs `requirements.txt`, imports the FastAPI application, and runs pytest. Any failed command causes the workflow to fail.

The CI configuration is part of the repository; this document does not claim a hosted GitHub Actions run passed unless that run is visible in GitHub Actions.

## Docker Evidence

The repository includes:

- root `Dockerfile` for the FastAPI backend
- `frontend/Dockerfile` for the static frontend
- `compose.yaml` to run both services
- `.dockerignore`

Expected command:

```bash
docker compose up --build
```

The configuration was reviewed for consistent ports, paths, and service roles. A Docker runtime was not available in the verification environment, so no fabricated container-run result is reported.

## Release Checklist

- Required final documentation names exist.
- README contains a `Final Project` section.
- Null-title updates are rejected with HTTP 422.
- Regression coverage verifies the stored title is preserved after rejection.
- Full current test file passes: 34 tests.
- Forward-only task status progression remains enforced.
- CI and Docker configuration remain present.
- No real secrets are introduced by these changes.
