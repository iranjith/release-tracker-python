from fastapi import FastAPI, Response, status
from sqlalchemy.exc.IntegrityError import IntegrityError

from .routers import projects

app = FastAPI(
    title="Release Tracker API",
    description="A simple release tracker API",
    version="1.0.0",
)


app.include_router(projects.router)


@app.exception_handler(IntegrityError)
def handle_integrity_error(request, exc: IntegrityError):
    return Response(
        content="Integrity error: Duplicate entry or constraint violation.",
        status_code=status.HTTP_409_CONFLICT,
    )


@app.get("/")
def root():
    return {"message": "Welcome to the Release Tracker API!"}
