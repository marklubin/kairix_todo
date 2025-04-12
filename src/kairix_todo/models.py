import uuid
from datetime import date, datetime
from typing import List

from marshmallow import Schema, fields, post_load, validate
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)


# Base setup
class Base(DeclarativeBase):
    pass


# Many-to-many relationship table
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", String, ForeignKey("tasks.id")),
    Column("tag_id", String, ForeignKey("tags.id")),
)


# Tag model
class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    tasks: Mapped[List["Task"]] = relationship(
        "Task", secondary=task_tags, back_populates="tags"
    )

    @validates("name")
    def validate_name(self, key: str, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Tag name cannot be empty")
        return value


# Task model
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    due_date: Mapped[date] = mapped_column(Date, nullable=True)
    additional_details: Mapped[str] = mapped_column(String(256), nullable=True)

    tags: Mapped[List[Tag]] = relationship(
        "Tag", secondary=task_tags, back_populates="tasks"
    )
    reminders: Mapped[List["Reminder"]] = relationship(
        "Reminder", back_populates="task"
    )

    @validates("title")
    def validate_title(self, key: str, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        return value


# Reminder model
class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    task_id: Mapped[str] = mapped_column(String, ForeignKey("tasks.id"), nullable=False)
    remind_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    task: Mapped["Task"] = relationship("Task", back_populates="reminders")


# Marshmallow schemas
class TagSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))

    @post_load
    def make_tag(self, data, **kwargs):
        return Tag(**data)


class TaskSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    completed = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    due_date = fields.Date(allow_none=True)
    additional_details = fields.Str(allow_none=True)

    tags = fields.List(fields.Nested(TagSchema), required=False)

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)


class ReminderSchema(Schema):
    id = fields.Str(dump_only=True)
    task_id = fields.Str(required=True)
    remind_at = fields.DateTime(required=True)
    completed = fields.Bool()

    @post_load
    def make_reminder(self, data, **kwargs):
        return Reminder(**data)
