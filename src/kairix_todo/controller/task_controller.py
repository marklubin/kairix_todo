from flask import Blueprint, abort, jsonify, request
from sqlalchemy.orm import Session

from kairix_todo.models import Tag, TagSchema, Task, TaskSchema


class TaskController:
    def __init__(self, session: Session):
        self.session = session
        self.blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")
        self.task_schema = TaskSchema()
        self.tasks_schema = TaskSchema(many=True)
        self.tag_schema = TagSchema()

        # Route definitions
        self.blueprint.route("/", methods=["POST"])(self.create_task)
        self.blueprint.route("/<task_id>/complete", methods=["PATCH"])(
            self.complete_task
        )
        self.blueprint.route("/<task_id>", methods=["PATCH"])(self.edit_task)
        self.blueprint.route("/<task_id>", methods=["DELETE"])(self.delete_task)
        self.blueprint.route("/<task_id>", methods=["GET"])(self.get_task)
        self.blueprint.route("/", methods=["GET"])(self.list_tasks)

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

        task.completed = True
        self.session.commit()

        return jsonify(self.task_schema.dump(task)), 200

    def edit_task(self, task_id: str):
        task = self.session.get(Task, task_id)
        if not task:
            abort(404, description="Task not found.")

        data = request.json

        assert data is not None, "Data cannot be None"
        tag_names = data.pop("tags", None)

        if tag_names is not None:
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
