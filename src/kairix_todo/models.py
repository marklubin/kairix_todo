import uuid
from datetime import date, datetime

from marshmallow import Schema, fields, post_load
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Index, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

Base = declarative_base()

# Association table for many-to-many relationship between Task and Tag
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", String, ForeignKey("tasks.id")),
    Column("tag_id", String, ForeignKey("tags.id")),
)


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_task_title", "title"),
        Index("idx_task_due_date", "due_date"),
        Index("idx_task_completed", "completed"),
        {"sqlite_autoincrement": True, "sqlite_with_rowid": True},
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    additional_details = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(Date, nullable=True)

    # Relationships
    reminders = relationship("Reminder", back_populates="task")
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")

    @validates("title")
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        return value

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)

    # Relationships
    tasks = relationship("Task", secondary=task_tags, back_populates="tags")

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        return value

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    remind_at = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)

    # Relationships
    task = relationship("Task", back_populates="reminders")

    def __repr__(self):
        return f"<Reminder(id={self.id}, task_id='{self.task_id}', remind_at='{self.remind_at}')>"


# Marshmallow schemas for serialization/deserialization
class TagSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

    @post_load
    def make_tag(self, data, **kwargs):
        return Tag(**data)


class ReminderSchema(Schema):
    id = fields.Str(dump_only=True)
    task_id = fields.Str(required=True)
    remind_at = fields.DateTime(required=True)
    completed = fields.Bool()

    @post_load
    def make_reminder(self, data, **kwargs):
        return Reminder(**data)


class TaskSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    additional_details = fields.Str()
    completed = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    due_date = fields.Date()
    tags = fields.List(fields.Nested(TagSchema))
    reminders = fields.List(fields.Nested(ReminderSchema))

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)
