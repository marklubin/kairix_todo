"""Utilities for searching tasks with various filters."""

from datetime import date, datetime
from typing import Any, List, Optional, Tuple, Union

from sqlalchemy import or_

from kairix_todo.models import Task


def search_tasks(
    session: Any,
    query: Optional[str] = None,
    from_date: Optional[Union[str, date, datetime]] = None,
    to_date: Optional[Union[str, date, datetime]] = None,
    completed: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
) -> Tuple[List[Task], int]:
    """Search for tasks with various filters.

    Args:
        session: SQLAlchemy database session
        query: Text to search in title and description
        from_date: Filter tasks due on or after this date
        to_date: Filter tasks due on or before this date
        completed: Filter by completion status
        limit: Maximum number of results to return
        offset: Number of results to skip

    Returns:
        Tuple of (tasks, total_count)
    """
    task_query = session.query(Task)

    # Text search
    if query:
        task_query = task_query.filter(
            or_(
                Task.title.ilike(f"%{query}%"),
                Task.additional_details.ilike(f"%{query}%"),
            )
        )

    # Date filtering
    if from_date:
        # Convert datetime to date if needed
        if isinstance(from_date, datetime):
            from_date = from_date.date()
        task_query = task_query.filter(Task.due_date >= from_date)
    if to_date:
        # Convert datetime to date if needed
        if isinstance(to_date, datetime):
            to_date = to_date.date()
        task_query = task_query.filter(Task.due_date <= to_date)

    # Completion status
    if completed is not None:
        task_query = task_query.filter(Task.completed == completed)

    # Get total count before pagination
    total_count = task_query.count()

    # Apply pagination
    tasks = task_query.limit(limit).offset(offset).all()

    return tasks, total_count
