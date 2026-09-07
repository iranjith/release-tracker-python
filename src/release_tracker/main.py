from fastapi import FastAPI, HTTPException, Response, status

from release_tracker import crud

from .dependencies import SessionDep
from .models import ProjectCreate, ProjectRead, ProjectUpdate

app = FastAPI(
    title="Release Tracker API",
    description="A simple release tracker API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to the Release Tracker API!"}


@app.get("/projects/{project_id}", response_model=ProjectRead | None)
def get_project(project_id: int, session: SessionDep):
    project = crud.get_project(session, project_id)
    return project


@app.get("/projects", response_model=list[ProjectRead])
def list_projects(session: SessionDep):
    return crud.list_projects(session)


@app.post(
    "/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED
)
def create_project(project_create: ProjectCreate, session: SessionDep):
    project = crud.create_project(session, project_create)
    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: SessionDep):
    project = crud.get_project(session, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    crud.delete_project(session, project)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, project_update: ProjectUpdate, session: SessionDep
):
    project = crud.get_project(session, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return crud.update_project(session, project, project_update)
