from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app.business_rules import validate_status_transition
from app.models import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)
from app.storage import (
    add_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
)

load_dotenv()

app = FastAPI(
    title="Task Tracker API",
    description="A learning-project Task Tracker built through Modules 1-3.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=200)
def health_check() -> dict[str, str]:
    """Return the current health status of the API."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(payload: TaskCreate) -> TaskResponse:
    return add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    task_status: TaskStatus | None = Query(default=None, alias="status"),
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
    tag: str | None = None,
) -> list[TaskResponse]:
    tasks = get_all_tasks()
    if task_status is not None:
        tasks = [task for task in tasks if task.status == task_status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if overdue is not None:
        tasks = [task for task in tasks if task.is_overdue is overdue]
    if tag is not None:
        normalized_tag = tag.strip().casefold()
        tasks = [
            task
            for task in tasks
            if any(item.casefold() == normalized_tag for item in task.tags)
        ]
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: str) -> TaskResponse:
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    current = get_task_by_id(task_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if "status" in payload.model_fields_set and payload.status is not None:
        try:
            validate_status_transition(current.status, payload.status)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    changes = payload.model_dump(exclude_unset=True)
    updated = update_task(task_id, changes)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: str) -> Response:
    if not delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
