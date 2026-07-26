import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import _reset


@pytest.fixture(autouse=True)
def reset_storage():
    _reset()
    yield
    _reset()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_task(client):
    response = client.post("/tasks", json={"title": "Test task"})
    assert response.status_code == 201
    return response.json()
