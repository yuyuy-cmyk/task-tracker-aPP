from datetime import datetime, timezone
from uuid import uuid4

from app.models import TaskCreate, TaskResponse


_tasks: dict[str, TaskResponse] = {}


def add_task(task: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    stored = TaskResponse(
        id=str(uuid4()),
        created_at=now,
        updated_at=now,
        **task.model_dump(),
    )
    _tasks[stored.id] = stored
    return stored


def get_all_tasks() -> list[TaskResponse]:
    return list(_tasks.values())


def get_task_by_id(task_id: str) -> TaskResponse | None:
    return _tasks.get(task_id)


def update_task(task_id: str, changes: dict) -> TaskResponse | None:
    current = _tasks.get(task_id)
    if current is None:
        return None

    updated = current.model_copy(
        update={**changes, "updated_at": datetime.now(timezone.utc)}
    )
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()
