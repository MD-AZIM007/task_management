from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# -------------------------
# GET TESTS
# -------------------------

def test_get_all_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_success():
    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_task_not_found():
    response = client.get("/tasks/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# -------------------------
# POST TESTS
# -------------------------

def test_create_task_success():
    new_task = {
        "id": 100,
        "title": "Test FastAPI",
        "description": "Practice FastAPI testing",
        "status": "Pending",
        "priority": 3
    }

    response = client.post("/tasks", json=new_task)

    assert response.status_code == 201
    assert response.json()["id"] == 100
    assert response.json()["title"] == "Test FastAPI"


def test_create_task_duplicate_id():
    new_task = {
        "id": 1,
        "title": "Duplicate Task",
        "description": "This ID already exists",
        "status": "Pending",
        "priority": 2
    }

    response = client.post("/tasks", json=new_task)

    assert response.status_code == 400
    assert response.json()["detail"] == "Task ID already exists"


def test_create_task_invalid_priority():
    new_task = {
        "id": 101,
        "title": "Invalid Task",
        "description": "Priority is invalid",
        "status": "Pending",
        "priority": 10
    }

    response = client.post("/tasks", json=new_task)

    assert response.status_code == 422


def test_create_task_missing_title():
    new_task = {
        "id": 102,
        "description": "Title is missing",
        "status": "Pending",
        "priority": 2
    }

    response = client.post("/tasks", json=new_task)

    assert response.status_code == 422


# -------------------------
# PUT TESTS
# -------------------------

def test_update_task_success():
    updated_task = {
        "id": 1,
        "title": "Updated Task",
        "description": "Updated description",
        "status": "Completed",
        "priority": 4
    }

    response = client.put("/tasks/1", json=updated_task)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["status"] == "Completed"


def test_update_task_not_found():
    updated_task = {
        "id": 999,
        "title": "Unknown Task",
        "description": "Task does not exist",
        "status": "Pending",
        "priority": 2
    }

    response = client.put("/tasks/999", json=updated_task)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# -------------------------
# DELETE TESTS
# -------------------------

def test_delete_task_success():
    new_task = {
        "id": 200,
        "title": "Delete Me",
        "description": "This task will be deleted",
        "status": "Pending",
        "priority": 5
    }

    client.post("/tasks", json=new_task)

    response = client.delete("/tasks/200")

    assert response.status_code == 200
    assert response.json()["id"] == 200


def test_delete_task_not_found():
    response = client.delete("/tasks/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"