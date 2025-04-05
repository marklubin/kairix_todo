from datetime import date, datetime

import pytest
from sqlalchemy.orm import Session

from kairix_todo.models import Tag, Task


def test_task_creation(db_session: Session) -> None:
    task = Task(title="Test Task")
    db_session.add(task)
    db_session.commit()
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.completed is False
    assert isinstance(task.created_at, datetime)
    assert task.due_date is None
    assert task.additional_details is None
    assert task.tags == []


def test_task_creation_all_fields(db_session) -> None:
    due = date.today()
    task = Task(
        title="Task with Details",
        completed=True,
        due_date=due,
        additional_details="Additional info",
    )
    db_session.add(task)
    db_session.commit()
    assert task.title == "Task with Details"
    assert task.completed is True
    assert task.due_date == due
    assert task.additional_details == "Additional info"


def test_tag_creation(db_session) -> None:
    tag = Tag(name="Important")
    db_session.add(tag)
    db_session.commit()
    assert tag.id is not None
    assert tag.name == "Important"
    assert tag.tasks == []


def test_task_with_tags(db_session) -> None:
    task = Task(title="Task with Tags")
    tag1 = Tag(name="Urgent")
    tag2 = Tag(name="Home")

    task.tags.extend([tag1, tag2])

    db_session.add(task)
    db_session.add(tag1)
    db_session.add(tag2)
    db_session.commit()
    assert len(task.tags) == 2
    assert tag1 in task.tags
    assert tag2 in task.tags

    assert task in tag1.tasks
    assert task in tag2.tasks


def test_empty_task_title_error(db_session) -> None:
    with pytest.raises(Exception):
        # title is required and should not be empty
        db_session.add(Task(title=""))
        db_session.commit()


def test_empty_tag_name_error(db_session) -> None:
    with pytest.raises(Exception):
        db_session.add(Tag(name=""))  # name is required and should not be empty
        db_session.commit()
