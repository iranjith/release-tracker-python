from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from sqlmodel import Session, select

from release_tracker.database import get_session

from .models import Project, ProjectCreate, ProjectRead, ProjectUpdate


def slugify(value: str) -> str:
    cleaned = "-".join(c for c in value.lower() if c.isalnum() or c == " ")
    return "-".join(cleaned.split()) or "project"


app = FastAPI(
    title="Release Tracker API",
    description="A simple release tracker API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to the Release Tracker API!"}


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


@app.post(
    "/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED
)
def create_project(project_create: ProjectCreate, session: SessionDep):
    slug = slugify(project_create.name)
    project = Project.model_validate(project_create, update={"slug": slug})
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    session.delete(project)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, project_update: ProjectUpdate, session: SessionDep
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    updated_data = project_update.model_dump(exclude_unset=True)
    project.sqlmodel_update(updated_data)

    if "name" in updated_data:
        updated_data["slug"] = slugify(updated_data["name"])
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
