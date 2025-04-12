from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        {'sqlite_autoincrement': True},
        {'sqlite_with_rowid': True},
        {'fts5': 'title, description'}
    )

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)

    # Relationships
    reminders = relationship("Reminder", back_populates="task")

# Other models remain unchanged
