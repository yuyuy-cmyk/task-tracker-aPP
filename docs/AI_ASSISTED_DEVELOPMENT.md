# AI-Assisted Development

## Where AI/Codex was used

AI assistance was used as an engineering partner for the final-release hardening work. It helped inspect the repository, compare the implementation with the assignment requirements, identify missing release artifacts, review business rules, design regression coverage, prepare CI and Docker configuration, and draft repository-specific documentation.

## How AI output was reviewed

AI suggestions were not treated as proof. Repository files were inspected before changes were proposed. Behavior changes were checked against the existing application and tests. The completed-task transition issue was reproduced with an executable regression test before the business-rule table was changed.

## Important decisions

- Preserve the existing in-memory storage architecture instead of introducing SQLite/SQLModel merely because an earlier project plan mentioned it.
- Keep the static vanilla frontend instead of adding a JavaScript framework or build system.
- Use simple GitHub Actions CI focused on dependency installation, application import, and pytest.
- Use separate lightweight backend and frontend Docker images with Compose for developer convenience.
- Fix `Done -> InProgress` because it contradicted the intended forward-only task lifecycle.

## Human judgment still required

A human maintainer remains responsible for understanding the architecture and business rules, reviewing changes before submission, interpreting course expectations, and deciding whether future requirements justify architecture changes. AI-generated text and code must remain explainable and testable.

## Verification principle

No command result should be recorded as passing unless it was actually executed. If an environment cannot run Docker or GitHub Actions, the limitation must be stated and only static validation should be claimed.
