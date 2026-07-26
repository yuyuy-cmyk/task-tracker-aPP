# Mid-Course User Stories

## Feature 1: Due dates and overdue filter

### DD-1 - Assign a due date

As a team member, I want to assign an optional due date when creating a task so
that I know when the work is expected.

Acceptance criteria:

- A valid ISO date (`YYYY-MM-DD`) is accepted by `POST /tasks`.
- A missing due date is accepted and returned as `null`.
- An invalid date string returns HTTP 422.

### DD-2 - Update a due date

As a team member, I want to add, replace, or clear a task's due date so that the
deadline stays accurate.

Acceptance criteria:

- `PATCH /tasks/{id}` updates a valid due date.
- Sending `null` clears the due date.
- Updating the due date does not change unrelated fields.

### DD-3 - Identify and filter overdue work

As a team member, I want overdue tasks to be marked and filterable so that I can
prioritize late work.

Acceptance criteria:

- A non-completed task with a date before today has `is_overdue=true`.
- A task due today, a future task, or a completed task is not overdue.
- `GET /tasks?overdue=true` returns only overdue tasks.
- The frontend shows an overdue pill and provides an overdue filter.

AI assumption corrected: the first design could have treated every past-due
task as overdue. Completed tasks are explicitly excluded because already
finished work should not remain in the urgent overdue queue.

## Feature 2: Tags and labels

### TG-1 - Add tags

As a team member, I want to add tags to a task so that I can describe its area
or context.

Acceptance criteria:

- Create accepts a list containing up to 10 tags.
- Leading and trailing whitespace is removed.
- Blank tags and tags longer than 30 characters return HTTP 422.

### TG-2 - Update tags safely

As a team member, I want to replace a task's tags without affecting other task
details so that its classification remains current.

Acceptance criteria:

- `PATCH /tasks/{id}` replaces tags when the `tags` field is provided.
- A separate title or priority update preserves existing tags.
- Case-insensitive duplicate tags are stored once.

### TG-3 - View and filter by tag

As a team member, I want tags displayed on cards and a tag filter so that I can
find related tasks quickly.

Acceptance criteria:

- Each stored tag appears as a chip on its task card.
- `GET /tasks?tag=backend` matches the tag case-insensitively.
- A tag with no matching tasks returns HTTP 200 with an empty list.

AI assumption corrected: tags were not stored as one comma-separated string.
The API uses a list so validation, exact matching, and frontend rendering remain
predictable. The modal alone converts comma-separated user input into that list.
