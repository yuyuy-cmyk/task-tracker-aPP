# Code Review

## Review findings

The final-release review focused on maintainability, correctness, and avoiding unnecessary rewrites.

### Preserved

- FastAPI route structure
- Pydantic validation approach
- in-memory storage
- vanilla static frontend
- existing endpoint and response shapes
- existing due-date and tag behavior

### Issue fixed

`app/business_rules.py` allowed `Done -> InProgress`. That made a completed task reversible even though the intended lifecycle is forward-only. The transition was removed and a regression test was added.

### Release improvements

- Added GitHub Actions CI.
- Added backend/frontend Dockerfiles and Compose.
- Added Docker and runtime ignore rules.
- Added `AGENTS.md` for future AI-assisted maintenance.
- Expanded repository documentation for architecture, testing, security, AI use, and final evaluation.

## Dependency review

The dependency set is small and matches the application: FastAPI, Uvicorn, Pydantic, python-dotenv, pytest, and HTTPX. No risky version upgrade or speculative dependency removal was introduced during final hardening.

## Maintainability conclusion

The project remains intentionally small. The final release emphasizes explicit rules, regression tests, reproducible commands, and documentation instead of architectural churn.
