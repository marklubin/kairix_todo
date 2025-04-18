"""Controller for task search functionality."""

from datetime import date

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session

from kairix_todo.utils.search_utils import search_tasks


class SearchController:
    """Controller for task search functionality."""

    def __init__(self, session: Session):
        """Initialize the search controller.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.blueprint = Blueprint("search", __name__, url_prefix="/tasks")

        # Route definitions
        self.blueprint.route("/search", methods=["GET"])(self.search)

    def search(self):
        """Search for tasks with various filters.

        Returns:
            JSON response with search results
        """
        # Parse query parameters
        query = request.args.get("q")

        from_date = request.args.get("from_date")
        if from_date:
            from_date = date.fromisoformat(from_date)

        to_date = request.args.get("to_date")
        if to_date:
            to_date = date.fromisoformat(to_date)

        completed = request.args.get("completed")
        if completed is not None:
            completed = completed.lower() == "true"

        limit = request.args.get("limit", 100, type=int)
        offset = request.args.get("offset", 0, type=int)

        # Execute search
        tasks, total = search_tasks(
            self.session,
            query=query,
            from_date=from_date,
            to_date=to_date,
            completed=completed,
            limit=limit,
            offset=offset,
        )

        # Format response
        return jsonify([self._format_task(task) for task in tasks])

    def _format_task(self, task):
        """Format a task for JSON response.

        Args:
            task: Task object

        Returns:
            Dictionary representation of the task
        """
        return {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "additional_details": task.additional_details,
            "reminders": [
                self._format_reminder(reminder) for reminder in task.reminders
            ],
        }

    def _format_reminder(self, reminder):
        """Format a reminder for JSON response.

        Args:
            reminder: Reminder object

        Returns:
            Dictionary representation of the reminder
        """
        return {
            "id": reminder.id,
            "task_id": reminder.task_id,
            "remind_at": reminder.remind_at.isoformat() if reminder.remind_at else None,
            "completed": reminder.completed,
        }
