# Mini ADR: Due Dates and Tags

## Decision

Due dates are represented as an optional Pydantic `date` and overdue status is
computed by the backend as `due_date < today` while the task is not `Done`.
The list endpoint accepts an optional `overdue` filter. Tags are represented as
a list of validated strings with a maximum of 10 tags and 30 characters per
tag. Tags are trimmed and de-duplicated case-insensitively, and the list
endpoint supports exact case-insensitive tag filtering. Both fields live in the
existing in-memory task model and use the existing create/update/storage flow.

## Alternatives considered

AI-assisted exploration suggested computing overdue status only in JavaScript,
storing tags as comma-separated text, introducing a separate tag entity, or
adding a database. Frontend-only overdue logic was rejected because API filters
and clients could disagree. Comma-separated backend storage was rejected
because it makes validation and exact matching fragile. A normalized tag table
and database were rejected as unnecessary for the course's in-memory scope.

## Consequences

The implementation is small, testable, and consistent across API and UI. The
computed overdue value changes naturally as dates pass without a scheduled
background job. The trade-off is that all data disappears after a server
restart, tag matching is exact rather than substring-based, and the server's
local calendar date defines "today." If the project grew, the next decisions
would be persistent storage and an explicit user or project timezone.
