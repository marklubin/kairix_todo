from datetime import datetime

from kairix_todo.models import Reminder, Tag, Task


def test_create_task(client, db_session):
    response = client.post(
        "/tasks/", json={"title": "My Test Task", "tags": ["work", "urgent"]}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "My Test Task"
    assert len(data["tags"]) == 2

    # Verify tags created
    tags = db_session.query(Tag).all()
    assert len(tags) == 2


def test_mark_task_complete(client, db_session):
    task = Task(title="Incomplete Task")
    db_session.add(task)
    db_session.commit()

    response = client.patch(f"/tasks/{task.id}/complete")
    assert response.status_code == 200
    data = response.get_json()
    assert data["completed"] is True


def test_edit_task(client, db_session):
    task = Task(title="Original Task")
    db_session.add(task)
    db_session.commit()

    response = client.patch(
        f"/tasks/{task.id}", json={"title": "Edited Task", "tags": ["home"]}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Edited Task"
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "home"


def test_delete_task(client, db_session):
    task = Task(title="Task to Delete")
    db_session.add(task)
    db_session.commit()

    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 204

    assert db_session.get(Task, task.id) is None


def test_get_task(client, db_session):
    task = Task(title="Fetch Me")
    db_session.add(task)
    db_session.commit()

    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Fetch Me"


def test_list_tasks(client, db_session):
    tasks = [Task(title="Task 1"), Task(title="Task 2")]
    db_session.add_all(tasks)
    db_session.commit()

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_search_tasks(client, db_session):
    task1 = Task(title="Searchable Task 1")
    task2 = Task(title="Searchable Task 2")
    db_session.add_all([task1, task2])
    db_session.commit()

    response = client.get("/tasks/search?q=Searchable")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_list_task_reminders(client, db_session):
    task = Task(title="Task with Reminders")
    db_session.add(task)
    db_session.commit()

    reminder = Reminder(
        task_id=task.id, remind_at=datetime.fromisoformat("2023-10-10T10:00:00")
    )
    db_session.add(reminder)
    db_session.commit()

    response = client.get(f"/tasks/{task.id}/reminders")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1


def test_create_task_reminder(client, db_session):
    task = Task(title="Task for Reminder")
    db_session.add(task)
    db_session.commit()

    response = client.post(
        f"/tasks/{task.id}/reminders", json={"remind_at": "2023-10-10T10:00:00"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["task_id"] == task.id


def test_update_reminder(client, db_session):
    task = Task(title="Task to Update Reminder")
    db_session.add(task)
    db_session.commit()

    reminder = Reminder(
        task_id=task.id, remind_at=datetime.fromisoformat("2023-10-10T10:00:00")
    )
    db_session.add(reminder)
    db_session.commit()

    response = client.put(
        f"/tasks/reminders/{reminder.id}", json={"remind_at": "2023-10-11T10:00:00"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "2023-10-11" in data["remind_at"]


def test_delete_reminder(client, db_session):
    task = Task(title="Task to Delete Reminder")
    db_session.add(task)
    db_session.commit()

    reminder = Reminder(
        task_id=task.id, remind_at=datetime.fromisoformat("2023-10-10T10:00:00")
    )
    db_session.add(reminder)
    db_session.commit()

    response = client.delete(f"/tasks/reminders/{reminder.id}")
    assert response.status_code == 204


def test_list_tags(client, db_session):
    tag1 = Tag(name="Work")
    tag2 = Tag(name="Personal")
    db_session.add_all([tag1, tag2])
    db_session.commit()

    response = client.get("/tags/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_create_tag(client, db_session):
    response = client.post("/tags/", json={"name": "New Tag"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "New Tag"


def test_get_tag(client, db_session):
    tag = Tag(name="Fetch Me")
    db_session.add(tag)
    db_session.commit()

    response = client.get(f"/tags/{tag.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Fetch Me"


def test_update_tag(client, db_session):
    tag = Tag(name="Old Tag")
    db_session.add(tag)
    db_session.commit()

    response = client.put(f"/tags/{tag.id}", json={"name": "Updated Tag"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Tag"


def test_delete_tag(client, db_session):
    tag = Tag(name="Tag to Delete")
    db_session.add(tag)
    db_session.commit()

    response = client.delete(f"/tags/{tag.id}")
    assert response.status_code == 204
