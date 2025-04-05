import uuid
from datetime import date, datetime
from typing import  List, Optional
from kairix_todo.models.tag import Tag


from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Base model for task operations."""

    title: str = Field(..., min_length=1)


class TaskCreate(TaskBase):
    """Model for creating a new task."""

    completed: bool = False
    due_date: Optional[date] = None
    additional_details: Optional[str] = None
    tag_ids: List[uuid.UUID] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """Model for updating an existing task."""

    title: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[date] = None
    additional_details: Optional[str] = None
    tag_ids: Optional[List[uuid.UUID]] = None

# Forward references for Task model

class Task(TaskBase):
    """Model for a task."""
    id: uuid.UUID
    completed: bool = False
    created_at: datetime
    due_date: Optional[date] = None
    additional_details: Optional[str] = None
    tags: List["Tag"] = Field(default_factory=list)
    model_config = {"from_attributes": True}
