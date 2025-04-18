"""Tests for the search utilities."""

from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from kairix_todo.models import Task
from kairix_todo.utils.search_utils import search_tasks


def test_search_by_title(db_session: Session) -> None:
    """Test searching tasks by title."""
    # Create test tasks
    task1 = Task(
        title="Meeting with team", additional_details="Discuss project progress"
    )
    task2 = Task(title="Buy groceries", additional_details="Milk, eggs, bread")
    task3 = Task(title="Team lunch", additional_details="At the Italian restaurant")

    db_session.add_all([task1, task2, task3])
    db_session.commit()

    # Search for tasks with "team" in the title
    results, count = search_tasks(db_session, query="team")

    # Should match task1 and task3
    assert count == 2
    assert len(results) == 2
    assert any(task.title == "Meeting with team" for task in results)
    assert any(task.title == "Team lunch" for task in results)


def test_search_by_description(db_session: Session) -> None:
    """Test searching tasks by description."""
    # Create test tasks
    task1 = Task(title="Meeting", additional_details="Discuss team project")
    task2 = Task(title="Shopping", additional_details="Buy team shirts")
    task3 = Task(title="Dinner", additional_details="With family")

    db_session.add_all([task1, task2, task3])
    db_session.commit()

    # Search for tasks with "team" in the description
    results, count = search_tasks(db_session, query="team")

    # Should match task1 and task2
    assert count == 2
    assert len(results) == 2
    assert any(task.title == "Meeting" for task in results)
    assert any(task.title == "Shopping" for task in results)


def test_search_case_insensitive(db_session: Session) -> None:
    """Test that search is case insensitive."""
    # Create test tasks
    task1 = Task(title="IMPORTANT meeting", additional_details="High priority")
    task2 = Task(title="Regular meeting", additional_details="Low priority")

    db_session.add_all([task1, task2])
    db_session.commit()

    # Search with different case
    results, count = search_tasks(db_session, query="important")

    # Should match task1
    assert count == 1
    assert len(results) == 1
    assert results[0].title == "IMPORTANT meeting"


def test_filter_by_completion_status(db_session: Session) -> None:
    """Test filtering tasks by completion status."""
    # Create test tasks
    task1 = Task(title="Completed task", additional_details="Done", completed=True)
    task2 = Task(
        title="Incomplete task", additional_details="Not done", completed=False
    )

    db_session.add_all([task1, task2])
    db_session.commit()

    # Filter for completed tasks
    results, count = search_tasks(db_session, completed=True)

    # Should match task1
    assert count == 1
    assert len(results) == 1
    assert results[0].title == "Completed task"

    # Filter for incomplete tasks
    results, count = search_tasks(db_session, completed=False)

    # Should match task2
    assert count == 1
    assert len(results) == 1
    assert results[0].title == "Incomplete task"


def test_filter_by_date_range(db_session: Session) -> None:
    """Test filtering tasks by due date range."""
    # Create test tasks
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)

    task1 = Task(title="Yesterday task", additional_details="Past", due_date=yesterday)
    task2 = Task(title="Tomorrow task", additional_details="Soon", due_date=tomorrow)
    task3 = Task(
        title="Next week task", additional_details="Future", due_date=next_week
    )

    db_session.add_all([task1, task2, task3])
    db_session.commit()

    # Filter for tasks due from today onwards
    results, count = search_tasks(db_session, from_date=today)

    # Should match task2 and task3
    assert count == 2
    assert len(results) == 2
    assert any(task.title == "Tomorrow task" for task in results)
    assert any(task.title == "Next week task" for task in results)

    # Filter for tasks due until tomorrow
    results, count = search_tasks(db_session, to_date=tomorrow)

    # Should match task1 and task2
    assert count == 2
    assert len(results) == 2
    assert any(task.title == "Yesterday task" for task in results)
    assert any(task.title == "Tomorrow task" for task in results)

    # Filter for tasks due between today and tomorrow
    results, count = search_tasks(db_session, from_date=today, to_date=tomorrow)

    # Should match task2
    assert count == 1
    assert len(results) == 1
    assert results[0].title == "Tomorrow task"


def test_pagination(db_session: Session) -> None:
    """Test pagination of search results."""
    # Create 10 test tasks
    tasks = [
        Task(title=f"Task {i}", additional_details=f"Description {i}")
        for i in range(1, 11)
    ]

    db_session.add_all(tasks)
    db_session.commit()

    # Get first page (limit 5)
    results, count = search_tasks(db_session, limit=5, offset=0)

    # Should return 5 tasks but count all 10
    assert count == 10
    assert len(results) == 5

    # Get second page (limit 5, offset 5)
    results, count = search_tasks(db_session, limit=5, offset=5)

    # Should return 5 tasks but count all 10
    assert count == 10
    assert len(results) == 5

    # Make sure first and second page results are different
    first_page, _ = search_tasks(db_session, limit=5, offset=0)
    second_page, _ = search_tasks(db_session, limit=5, offset=5)

    first_page_ids = [task.id for task in first_page]
    second_page_ids = [task.id for task in second_page]

    # No overlap between pages
    assert not any(task_id in second_page_ids for task_id in first_page_ids)


def test_combined_filters(db_session: Session) -> None:
    """Test combining multiple search filters."""
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
    task3 = Task(
        title="Important presentation",
        additional_details="Client meeting",
        completed=False,
        due_date=today,
    )

    db_session.add_all([task1, task2, task3])
    db_session.commit()

    # Search for incomplete important tasks due tomorrow
    results, count = search_tasks(
        db_session,
        query="important",
        completed=False,
        from_date=tomorrow,
        to_date=tomorrow,
    )

    # Should match only task1
    assert count == 1
    assert len(results) == 1
    assert results[0].title == "Important meeting"


def test_empty_results(db_session: Session) -> None:
    """Test search with no matching results."""
    # Create test tasks
    task1 = Task(title="Meeting", additional_details="Team discussion")
    task2 = Task(title="Lunch", additional_details="With colleagues")

    db_session.add_all([task1, task2])
    db_session.commit()

    # Search for non-existent term
    results, count = search_tasks(db_session, query="nonexistent")

    # Should return empty results
    assert count == 0
    assert len(results) == 0
