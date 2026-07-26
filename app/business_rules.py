from app.models import TaskStatus


VALID_TRANSITIONS = frozenset(
    {
        (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
    }
)


def validate_status_transition(
    current: TaskStatus, new: TaskStatus
) -> None:
    if (current, new) not in VALID_TRANSITIONS:
        raise ValueError(
            f"Invalid status transition from {current.value} to {new.value}"
        )
