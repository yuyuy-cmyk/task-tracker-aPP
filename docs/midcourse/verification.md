# Verification Evidence

Verification date: 26 July 2026

## Baseline

- Module 1 ZIP inspected: expected scaffold files were present.
- Python compilation: passed.
- `GET /health`: HTTP 200 with `status="ok"` and an ISO timestamp.
- `/docs`: HTTP 200 with `text/html`.
- `python -m tests.verify_a`: all 8 model checks printed `PASS`.

## Automated backend tests

Command:

```bash
pytest tests/ -v
```

Result: **32 passed**.

Coverage includes health, create/list/read/update/delete, empty and invalid
payloads, filtering, 404 behavior, transition rules, due dates, overdue
detection, completed-task handling, tag validation, tag updates, tag filtering,
and preservation after unrelated updates.

## End-to-end HTTP check

A live Uvicorn process accepted:

```json
{
  "title": "Course project",
  "priority": "High",
  "due_date": "2026-07-25",
  "tags": ["AUB", "backend"]
}
```

The API returned HTTP 201 with the supplied fields and `is_overdue=true`.

## Feature Break Tests

### Break Test 1 - Overdue comparison

Deliberate break: changed the overdue comparison from `due_date < today` to
`due_date > today`.

Command:

```bash
pytest tests/test_tasks.py::test_overdue_detection_and_filter -v
```

Observed failure: the response contained `["Later"]` instead of `["Late"]`.
The comparison was restored and the targeted test passed.

### Break Test 2 - Blank tag validation

Deliberate break: changed the tag validator to skip blank tags rather than
reject them.

Command:

```bash
pytest tests/test_tasks.py::test_empty_tag_returns_422 -v
```

Observed failure: expected HTTP 422 but received HTTP 201. The rejection was
restored and the targeted test passed.

Final result after both restorations: **32 passed**.

## Source behavior contract before and after focused frontend cleanup

| Contract item | Before | After |
| --- | --- | --- |
| Exact status values remain `ToDo`, `InProgress`, `Done` | PASS | PASS |
| Three Kanban columns and empty placeholders render | PASS | PASS |
| Cards sort High, Medium, Low | PASS | PASS |
| Loading and API error messages remain visible | PASS | PASS |
| Create uses POST and edit uses PATCH | PASS | PASS |
| Whitespace-only title sends no request | PASS | PASS |
| Invalid drag/edit displays the backend error and refreshes | PASS | PASS |
| Due date, overdue pill, tag chips, and filters remain wired | PASS | PASS |

The focused cleanup extracted repeated notice rendering into `setNotice()`.
Static inspection and a JavaScript syntax check confirmed that API constants,
selectors, methods, status strings, validation, and error paths stayed
unchanged. The automated backend suite also remained green.

## Manual browser checklist (local run required)

The remote verification browser could not access the workspace's localhost.
Run the backend and frontend using the README, then mark these checks during the
local browser run:

- three columns appear and priority order is High, Medium, Low;
- create and edit refresh the board;
- valid drag-and-drop persists;
- an invalid transition shows a message and refreshes;
- empty-title submission stays in the modal without a request;
- past unfinished work displays an overdue pill;
- overdue and tag filters return only matching cards;
- Cancel, close, Escape, and overlay click dismiss the modal.
