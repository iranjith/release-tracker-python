from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Release Tracker API",
    description="A simple release tracker API",
    version="1.0.0",
)


class ProjectRead(BaseModel):
    id: int
    name: str
    slug: str


mock_projects = [
    ProjectRead(id=1, name="Project A", slug="project-a"),
    ProjectRead(id=2, name="Project B", slug="project-b"),
    ProjectRead(id=3, name="Project C", slug="project-c"),
]


@app.get("/projects/{project_id}", response_model=ProjectRead | None)
def get_project_by_id(project_id: int) -> ProjectRead | None:
    # In a real application, you would fetch the project from a database
    for project in mock_projects:
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        if project.id == project_id:
            return project

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
    )


@app.get("/projects", response_model=list[ProjectRead])
def list_projects(name: str | None = None) -> list[ProjectRead]:
    if name:
        return [project for project in mock_projects if project.name == name]
    return mock_projects
