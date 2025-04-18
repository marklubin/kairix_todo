"""Tests for the search controller."""

import json
from datetime import datetime, timedelta

import pytest
from flask.testing import FlaskClient

from kairix_todo.models import Task


def test_search_endpoint_basic(client: FlaskClient, db_session) -> None:
    """Test the basic search endpoint functionality."""
    # Create test tasks
    task1 = Task(
        title="Meeting with team", additional_details="Discuss project progress"
    )
    task2 = Task(title="Buy groceries", additional_details="Milk, eggs, bread")

    db_session.add_all([task1, task2])
    db_session.commit()

    # Search for tasks with "team" in the title or description
    response = client.get("/tasks/search?q=team")

    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify results
    assert len(data) == 1
    assert data[0]["title"] == "Meeting with team"


def test_search_with_completion_filter(client: FlaskClient, db_session) -> None:
    """Test searching with completion status filter."""
    # Create test tasks
    task1 = Task(title="Completed task", additional_details="Done", completed=True)
    task2 = Task(
        title="Incomplete task", additional_details="Not done", completed=False
    )

    db_session.add_all([task1, task2])
    db_session.commit()

    # Search for completed tasks
    response = client.get("/tasks/search?completed=true")

    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify results
    assert len(data) == 1
    assert data[0]["title"] == "Completed task"
    assert data[0]["completed"] is True


def test_search_with_date_filters(client: FlaskClient, db_session) -> None:
    """Test searching with date filters."""
    # Create test tasks
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    task1 = Task(title="Yesterday task", additional_details="Past", due_date=yesterday)
    task2 = Task(title="Tomorrow task", additional_details="Future", due_date=tomorrow)

    db_session.add_all([task1, task2])
    db_session.commit()

    # Format dates for URL
    from_date = today.strftime("%Y-%m-%d")

    # Search for tasks due from today onwards
    response = client.get(f"/tasks/search?from_date={from_date}")

    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify results
    assert len(data) == 1
    assert data[0]["title"] == "Tomorrow task"


def test_search_with_pagination(client: FlaskClient, db_session) -> None:
    """Test search pagination."""
    # Create 10 test tasks
    tasks = [
        Task(title=f"Task {i}", additional_details=f"Description {i}")
        for i in range(1, 11)
    ]

    db_session.add_all(tasks)
    db_session.commit()

    # Get first page (limit 5)
    response = client.get("/tasks/search?limit=5&offset=0")

    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify results
    assert len(data) == 5

    # Get second page (limit 5, offset 5)
    response = client.get("/tasks/search?limit=5&offset=5")

    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify results
    assert len(data) == 5


def test_search_with_combined_filters(client: FlaskClient, db_session) -> None:
    """Test searching with combined filters."""
    # Create test tasks
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    task1 = Task(
        title="Important meeting",
        additional_details="Team discussion",
        completed=False,
        due_date=tomorrow,
    )
    task2 = Task(
        title="Team lunch",
        additional_details="Important celebration",
        completed=True,
        due_date=tomorrow,
    )

    db_session.add_all([task1, task2])
    db_session.commit()

    # Format dates for URL
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    # Search for incomplete tasks with "important" in the title or description due tomorrow
    response = client.get(
        f"/tasks/search?q=important&completed=false&from_date={tomorrow_str}&to_date={tomorrow_str}"
    )

    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify results
    assert len(data) == 1
    assert data[0]["title"] == "Important meeting"
    assert data[0]["completed"] is False


def test_search_no_results(client: FlaskClient, db_session) -> None:
    """Test search with no matching results."""
    # Create test tasks
    task = Task(title="Meeting", additional_details="Team discussion")

    db_session.add(task)
    db_session.commit()

    # Search for non-existent term
    response = client.get("/tasks/search?q=nonexistent")

    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify empty results
    assert len(data) == 0


def test_search_response_format(client: FlaskClient, db_session) -> None:
    """Test the format of the search response."""
    # Create a task with reminders
    task = Task(
        title="Test task",
        additional_details="Test description",
        completed=False,
        due_date=datetime.now(),
    )

    db_session.add(task)
    db_session.commit()

    # Search for the task
    response = client.get("/tasks/search?q=test")

    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify task format
    assert len(data) == 1
    task_data = data[0]

    # Check all expected fields are present
    assert "id" in task_data
    assert "title" in task_data
    assert "additional_details" in task_data
    assert "completed" in task_data
    assert "created_at" in task_data
    assert "due_date" in task_data
    assert "reminders" in task_data

    # Check field values
    assert task_data["title"] == "Test task"
    assert task_data["additional_details"] == "Test description"
    assert task_data["completed"] is False
    assert task_data["reminders"] == []
