from fastapi import FastAPI

app = FastAPI(
    title="Release Tracker API",
    description="A simple release tracker API",
    version="1.0.0",
)


@app.get("/projects")
def list_projects() -> list[dict]:
    return [
        {
            "id": 1,
            "name": "Project A",
        },
        {
            "id": 2,
            "name": "Project B",
        },
        {
            "id": 3,
            "name": "Project C",
        },
    ]
