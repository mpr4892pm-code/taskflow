from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    projects = relationship(
        "Project",
        back_populates="owner",
        cascade="all, delete"
    )


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_name = Column(
        String(150),
        nullable=False
    )

    description = Column(Text)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="projects"
    )

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(Text)

    priority = Column(
        String(20),
        nullable=False
    )

    due_date = Column(
        String(255),
        nullable=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.project_id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )

    __table_args__ = (
        CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="check_priority"
        ),
    )