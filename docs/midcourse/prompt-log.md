# AI Prompt Log

The prompts below adapt the course libraries' four-part structure: role/context,
task, constraints, and output format. The recorded decisions describe what was
accepted, edited, or rejected during this implementation.

## Feature 1: Due dates and overdue filter

### Prompt DD-1 - User stories and assumptions

> You are a product owner extending a FastAPI Task Tracker. Add a small due-date
> and overdue-filter feature. Generate three user stories with testable
> acceptance criteria for backend and frontend behavior. The due date must
> remain optional. Do not add notifications, scheduling, authentication, a
> database, or deployment. List assumptions separately.

AI returned stories for create, update, overdue display, and filtering. I
accepted the small end-to-end scope. I edited the overdue rule to exclude
completed tasks and rejected reminders and notifications as out of scope.

### Prompt DD-2 - Focused backend implementation

> You are a senior FastAPI/Pydantic v2 developer. Inspect the existing
> `app/models.py`, `app/storage.py`, and `app/main.py`. Add optional `due_date`
> support to create, response, and partial update models. Compute `is_overdue`
> in the backend and add an optional `overdue` query filter to the existing
> `GET /tasks`. Preserve the current helper names, CRUD status codes, transition
> rules, and in-memory architecture. Do not rewrite unrelated files. Return a
> concise file-by-file change plan before code.

AI proposed a Pydantic `date` and backend-computed flag. I accepted those
choices. I rejected a scheduled job and retained the existing storage helpers.

### Prompt DD-3 - Tests and Break Test

> Review the current pytest fixture pattern and propose focused tests for valid
> and invalid dates, overdue detection, completed past-due tasks, due-date
> updates, and `overdue=true` filtering. Generate only the selected tests. Then
> identify one minimal production-code mutation that should make the overdue
> test fail. Do not weaken existing assertions.

AI returned the relevant date cases. I accepted them and deliberately reversed
the date comparison. The selected test failed by returning `Later` instead of
`Late`; after restoring `<`, it passed.

## Feature 2: Tags and labels

### Weak prompt

> Add tags to tasks and make them filterable.

Review: this does not define storage shape, whitespace behavior, duplicates,
limits, matching semantics, files, UI behavior, or expected tests. It could
produce incompatible or overbuilt code.

### Rewritten strong prompt TG-1 - Requirements and model

> You are a senior FastAPI/Pydantic v2 developer extending an in-memory Task
> Tracker. Add `tags` as a list of strings to create, update, and response
> models. Trim each tag, reject blank tags, allow at most 10 tags with 30
> characters each, and remove case-insensitive duplicates while preserving
> first-seen spelling and order. An unrelated PATCH must preserve existing
> tags. Do not add a database, tag IDs, a tag table, or new dependencies. Return
> assumptions and a focused patch only.

AI returned list-based validation. I accepted it after making duplicate
handling explicit. I rejected normalized database entities as out of scope.

### Prompt TG-2 - API and frontend integration

> Extend the existing `GET /tasks` with an optional exact, case-insensitive
> `tag` filter. Update only the existing vanilla JavaScript modal, cards, and
> filter controls so comma-separated user input becomes a JSON tag list and
> stored tags render as chips. Preserve status strings, URLs, methods,
> drag-and-drop behavior, due-date behavior, and 422 error display. Do not
> rewrite the application architecture.

AI returned the API filter and focused UI changes. I accepted exact matching and
client-side comma parsing. I rejected substring search because the assignment
asks for tag filtering, not general text search.

### Prompt TG-3 - Tests and Break Test

> Using the existing synchronous TestClient fixtures, add tests for creating
> tags, rejecting a blank tag, updating tags, case-insensitive tag filtering,
> and preserving tags after an unrelated update. Then suggest one minimal
> deliberate source break that proves the blank-tag test is meaningful. Keep
> all existing tests unchanged.

AI suggested bypassing blank-tag rejection. I temporarily skipped blank tags;
the test failed because the API returned 201 instead of 422. I restored the
validator and the complete suite returned green.
