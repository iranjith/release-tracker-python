from fastapi import APIRouter, Response, status

from .. import crud
from ..dependencies import ProjectDep, SessionDep
from ..models import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/projects", response_model=list[ProjectRead])
def list_projects(session: SessionDep):
    return crud.list_projects(session)


@router.get("/{project_id}", response_model=ProjectRead | None)
def get_project(project: ProjectDep):
    return project


@router.post(
    "/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED
)
def create_project(project_create: ProjectCreate, session: SessionDep):
    project = crud.create_project(session, project_create)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project: ProjectDep, session: SessionDep):
    crud.delete_project(session, project)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project: ProjectDep, project_update: ProjectUpdate, session: SessionDep
):
    return crud.update_project(session, project, project_update)
