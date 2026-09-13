from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated

from pydantic import StringConstraints
from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class TaskStatus(StrEnum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


def utc_now() -> datetime:
    return datetime.now(UTC)


ProjectName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2),
]

TaskName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2),
]


class TaskBase(SQLModel):
    name: TaskName
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    project: Project = Relationship(back_populates="tasks")


class ProjectBase(SQLModel):
    name: ProjectName = Field(unique=True)
    description: str | None = None


class Project(ProjectBase, table=True):
    __tablename__ = "projects"

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True)

    tasks: list[Task] = Relationship(back_populates="project")

    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: ProjectName = Field(default=None)
    description: str | None = None


class ProjectRead(ProjectBase):
    id: int
    slug: str
    created_at: datetime
