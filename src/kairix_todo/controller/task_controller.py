from datetime import datetime
from kairix_todo.utils.auth import check_api_key

from flask import Blueprint, abort, jsonify, request
from sqlalchemy.orm import Session

from kairix_todo.models import Reminder, ReminderSchema, Tag, Task, TaskSchema


class TaskController:
    def __init__(self, session: Session):
        self.session = session
        self.blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")
        self.blueprint.before_request(check_api_key)
        self.task_schema = TaskSchema()
        self.tasks_schema = TaskSchema(many=True)
        self.reminder_schema = ReminderSchema()
        self.reminders_schema = ReminderSchema(many=True)

        # Route definitions
        self.blueprint.route("/", methods=["POST"])(self.create_task)
        self.blueprint.route("/<task_id>/complete", methods=["PATCH"])(
            self.complete_task
        )
        self.blueprint.route("/<task_id>", methods=["PATCH"])(self.edit_task)
        self.blueprint.route("/<task_id>", methods=["DELETE"])(self.delete_task)
        self.blueprint.route("/<task_id>", methods=["GET"])(self.get_task)
        self.blueprint.route("/", methods=["GET"])(self.list_tasks)
        self.blueprint.route("/<task_id>/reminders", methods=["GET"])(
            self.list_task_reminders
        )
        self.blueprint.route("/<task_id>/reminders", methods=["POST"])(
            self.create_task_reminder
        )
        self.blueprint.route("/reminders/<reminder_id>", methods=["PUT"])(
            self.update_reminder
        )
        self.blueprint.route("/reminders/<reminder_id>", methods=["DELETE"])(
            self.delete_reminder
        )

    def get_or_create_tags(self, tag_names: list[str]) -> list[Tag]:
        tags = []
        for name in tag_names:
            tag = self.session.query(Tag).filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                self.session.add(tag)
        # Flush here to ensure tags have IDs if needed
        self.session.flush()
        tags = self.session.query(Tag).filter(Tag.name.in_(tag_names)).all()
        return tags

    def create_task(self):
        data = request.json
        if data is None:  # Check if data is not None
            abort(400, description="Invalid input data.")

        tag_names = data.pop("tags", [])
        tags = self.get_or_create_tags(tag_names)

        task = Task(**data)
        task.tags = tags

        self.session.add(task)
        self.session.commit()

        return jsonify(self.task_schema.dump(task)), 201

    def complete_task(self, task_id: str):
        task = self.session.get(Task, task_id)
        if not task:
            abort(404, description="Task not found.")

        task.completed = True  # type: ignore[assignment]
        self.session.commit()

        return jsonify(self.task_schema.dump(task)), 200

    def edit_task(self, task_id: str):
        task = self.session.get(Task, task_id)
        if not task:
            abort(404, description="Task not found.")

        data = request.json
        if data is None:  # Check if data is not None
            abort(400, description="Invalid input data.")

        tag_names = data.pop("tags", [])
        if tag_names:  # Check if tag_names is not empty
            task.tags = self.get_or_create_tags(tag_names)

        for key, value in data.items():
            setattr(task, key, value)

        self.session.commit()
        return jsonify(self.task_schema.dump(task)), 200

    def delete_task(self, task_id: str):
        task = self.session.get(Task, task_id)
        if not task:
            abort(404, description="Task not found.")

        self.session.delete(task)
        self.session.commit()

        return jsonify({"message": "Task deleted"}), 204

    def get_task(self, task_id: str):
        task = self.session.get(Task, task_id)
        if not task:
            abort(404, description="Task not found.")

        return jsonify(self.task_schema.dump(task)), 200

    def list_tasks(self):
        tasks = self.session.query(Task).all()
        return jsonify(self.tasks_schema.dump(tasks)), 200

    def list_task_reminders(self, task_id: str):
        task = self.session.get(Task, task_id)
        if not task:
            abort(404, description="Task not found.")

        reminders = task.reminders
        return jsonify(self.reminders_schema.dump(reminders)), 200

    def create_task_reminder(self, task_id: str):
        task = self.session.get(Task, task_id)
        if not task:
            abort(404, description="Task not found.")

        data = request.json
        if data is None:
            abort(400, description="Invalid input data.")
        assert isinstance(data, dict)
        raw_remind_at = data.get("remind_at")
        if raw_remind_at is not None:
            if isinstance(raw_remind_at, str):
                data["remind_at"] = datetime.fromisoformat(
                    raw_remind_at.replace("Z", "+00:00")
                )
            else:
                abort(
                    400,
                    description="Invalid remind_at format. Expected ISO 8601 string.",
                )

        reminder = Reminder(**data)
        reminder.task_id = task_id  # type: ignore[assignment]
        self.session.add(reminder)
        self.session.commit()

        return jsonify(self.reminder_schema.dump(reminder)), 201

    def update_reminder(self, reminder_id: str):
        reminder = self.session.get(Reminder, reminder_id)
        if not reminder:
            abort(404, description="Reminder not found.")

        data = request.json
        if data is None:
            abort(400, description="Invalid input data.")
        assert isinstance(data, dict)
        raw_remind_at = data.get("remind_at")
        if isinstance(raw_remind_at, str):
            data["remind_at"] = datetime.fromisoformat(
                raw_remind_at.replace("Z", "+00:00")
            )

        for key, value in data.items():
            setattr(reminder, key, value)

        self.session.commit()
        return jsonify(self.reminder_schema.dump(reminder)), 200

    def delete_reminder(self, reminder_id: str):
        reminder = self.session.get(Reminder, reminder_id)
        if not reminder:
            abort(404, description="Reminder not found.")

        self.session.delete(reminder)
        self.session.commit()
        return jsonify({"message": "Reminder deleted"}), 204
