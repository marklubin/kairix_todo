from kairix_todo.models import Tag, Task


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
