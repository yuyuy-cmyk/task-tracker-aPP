# Testing and Verification

## Scope

The pytest suite verifies the existing Task Tracker behavior rather than inventing new features. Coverage includes:

- health endpoint
- task creation and defaults
- title trimming and validation
- rejection of missing/blank titles and unknown fields
- task listing and retrieval
- status, priority, overdue, and tag filtering
- partial updates
- missing-resource errors
- invalid priority and status behavior
- status-transition business rules
- deletion
- due-date parsing and overdue calculation
- tag normalization, validation, updates, and persistence

## Regression added for final release

The release review found that `Done -> InProgress` was allowed even though completed tasks are intended to be terminal. A regression test was added to prove that a completed task cannot move backward.

## Commands

```bash
python -m pip install -r requirements.txt
python -c "from app.main import app; print(app.title, app.version)"
python -m pytest tests/ -q
python -m tests.verify_a
```

CI runs the application import check and pytest automatically on pushes to the main course branches and on pull requests.

## Verified result during final-release work

A local targeted verification reproducing the current API behavior initially failed on the completed-task rollback case. After fixing the transition table, that verification passed `9 passed in 0.10s`, and importing the FastAPI app succeeded as `Task Tracker API 1.0.0`.

The repository's full GitHub-hosted suite is also configured in CI. Do not copy CI results into this document unless the workflow actually runs successfully; the GitHub Actions page is the source of truth for hosted execution.
