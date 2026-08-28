from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select

from release_tracker.database import get_session

from .models import Project, ProjectRead

app = FastAPI(
    title="Release Tracker API",
    description="A simple release tracker API",
    version="1.0.0",
)

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/projects/{project_id}", response_model=ProjectRead | None)
def get_project_by_id(project_id: int, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@app.get("/projects", response_model=list[ProjectRead])
def list_projects(session: SessionDep):
    statement = select(Project).order_by(Project.name)
    projects = session.exec(statement).all()
    return list(projects)
