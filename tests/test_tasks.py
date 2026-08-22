from datetime import date, timedelta


def test_health_returns_status_and_timestamp(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["timestamp"]


def test_create_task_returns_201_and_defaults(client):
    response = client.post("/tasks", json={"title": "  Build API  "})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Build API"
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert body["description"] == ""
    assert body["tags"] == []


def test_create_missing_title_returns_422(client):
    assert client.post("/tasks", json={}).status_code == 422


def test_create_blank_title_returns_422(client):
    assert client.post("/tasks", json={"title": "   "}).status_code == 422


def test_create_rejects_extra_field(client):
    response = client.post("/tasks", json={"title": "Task", "unknown": True})
    assert response.status_code == 422


def test_list_empty_returns_200_with_empty_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_returns_created_tasks(client, created_task):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [created_task["id"]]


def test_list_filters_by_status(client):
    client.post("/tasks", json={"title": "Todo"})
    client.post("/tasks", json={"title": "Doing", "status": "InProgress"})
    response = client.get("/tasks", params={"status": "InProgress"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Doing"]


def test_list_filters_by_priority(client):
    client.post("/tasks", json={"title": "High", "priority": "High"})
    client.post("/tasks", json={"title": "Low", "priority": "Low"})
    response = client.get("/tasks", params={"priority": "High"})
    assert [task["title"] for task in response.json()] == ["High"]


def test_list_no_filter_match_returns_empty_list(client, created_task):
    response = client.get("/tasks", params={"priority": "High"})
    assert response.status_code == 200
    assert response.json() == []


def test_get_existing_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]


def test_get_missing_task_returns_404(client):
    assert client.get("/tasks/missing").status_code == 404


def test_patch_title_only_succeeds(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"title": "Updated"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_patch_missing_task_returns_404(client):
    assert client.patch("/tasks/missing", json={"title": "Updated"}).status_code == 404


def test_patch_empty_payload_returns_422(client, created_task):
    assert client.patch(f"/tasks/{created_task['id']}", json={}).status_code == 422


def test_patch_invalid_priority_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"priority": "Urgent"}
    )
    assert response.status_code == 422


def test_valid_status_transition_succeeds(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"status": "InProgress"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_invalid_status_transition_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"status": "Done"}
    )
    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_backward_status_transition_returns_422(client, created_task):
    task_id = created_task["id"]
    assert client.patch(f"/tasks/{task_id}", json={"status": "InProgress"}).status_code == 200
    response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert response.status_code == 422


def test_same_status_transition_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"status": "ToDo"}
    )
    assert response.status_code == 422


def test_done_task_cannot_move_back_to_in_progress(client, created_task):
    task_id = created_task["id"]
    assert client.patch(f"/tasks/{task_id}", json={"status": "InProgress"}).status_code == 200
    assert client.patch(f"/tasks/{task_id}", json={"status": "Done"}).status_code == 200
    response = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_delete_existing_task_returns_empty_204(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_task_returns_404(client):
    assert client.delete("/tasks/missing").status_code == 404


def test_create_with_valid_due_date(client):
    due_date = (date.today() + timedelta(days=3)).isoformat()
    response = client.post(
        "/tasks", json={"title": "Scheduled", "due_date": due_date}
    )
    assert response.status_code == 201
    assert response.json()["due_date"] == due_date
    assert response.json()["is_overdue"] is False


def test_invalid_due_date_format_returns_422(client):
    response = client.post(
        "/tasks", json={"title": "Bad date", "due_date": "tomorrow"}
    )
    assert response.status_code == 422


def test_overdue_detection_and_filter(client):
    past = (date.today() - timedelta(days=1)).isoformat()
    future = (date.today() + timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "Late", "due_date": past})
    client.post("/tasks", json={"title": "Later", "due_date": future})
    response = client.get("/tasks", params={"overdue": "true"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Late"]
    assert response.json()[0]["is_overdue"] is True


def test_completed_task_is_not_overdue(client):
    past = (date.today() - timedelta(days=1)).isoformat()
    response = client.post(
        "/tasks",
        json={"title": "Finished", "due_date": past, "status": "Done"},
    )
    assert response.json()["is_overdue"] is False


def test_update_due_date(client, created_task):
    due_date = (date.today() + timedelta(days=5)).isoformat()
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"due_date": due_date}
    )
    assert response.status_code == 200
    assert response.json()["due_date"] == due_date


def test_create_with_tags_normalizes_and_deduplicates(client):
    response = client.post(
        "/tasks", json={"title": "Tagged", "tags": [" API ", "api", "Backend"]}
    )
    assert response.status_code == 201
    assert response.json()["tags"] == ["API", "Backend"]


def test_empty_tag_returns_422(client):
    response = client.post(
        "/tasks", json={"title": "Tagged", "tags": ["valid", " "]}
    )
    assert response.status_code == 422


def test_update_tags(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"tags": ["frontend", "urgent"]}
    )
    assert response.status_code == 200
    assert response.json()["tags"] == ["frontend", "urgent"]


def test_filter_by_tag_is_case_insensitive(client):
    client.post("/tasks", json={"title": "API task", "tags": ["Backend"]})
    client.post("/tasks", json={"title": "UI task", "tags": ["Frontend"]})
    response = client.get("/tasks", params={"tag": "backend"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["API task"]


def test_tags_survive_unrelated_update(client):
    created = client.post(
        "/tasks", json={"title": "Tagged", "tags": ["keep-me"]}
    ).json()
    response = client.patch(
        f"/tasks/{created['id']}", json={"priority": "High"}
    )
    assert response.status_code == 200
    assert response.json()["tags"] == ["keep-me"]
