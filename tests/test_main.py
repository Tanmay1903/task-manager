# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import models, schemas, database

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the database dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_db] = override_get_db

# Create the test client
client = TestClient(app)

# Setup the database before running tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

def test_create_task():
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "id" in data

def test_get_tasks():
    # Create a task first
    response = client.post("/tasks/", json={"title": "Specific Task", "description": "Specific Description"})

    # Now fetch the tasks
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Ensure there's at least one task
    assert "title" in data[0]
    assert "description" in data[0]

def test_get_task_by_id():
    # Create a task first
    response = client.post("/tasks/", json={"title": "Specific Task", "description": "Specific Description"})
    task_id = response.json()["id"]

    # Now fetch the task by ID
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"
    assert data["description"] == "Specific Description"

def test_get_task_by_id_not_found():
    response = client.get("/tasks/9999")  # Assuming this ID doesn't exist
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task not found"

def test_update_task():
    # Create a task first
    response = client.post("/tasks/", json={"title": "Task to Update", "description": "Original Description"})
    task_id = response.json()["id"]

    # Update the task
    update_response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "description": "Updated Description"})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"

def test_update_task_not_found():
    response = client.put("/tasks/9999", json={"title": "Non-existent Task", "description": "No Description"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task not found"

def test_delete_task():
    # Create a task first
    response = client.post("/tasks/", json={"title": "Task to Delete", "description": "Delete this task"})
    task_id = response.json()["id"]

    # Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["id"] == task_id
    assert data["title"] == "Task to Delete"
    assert data["description"] == "Delete this task"

    # Try to get the deleted task
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_delete_task_not_found():
    response = client.delete("/tasks/9999")  # Assuming this ID doesn't exist
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task not found"
