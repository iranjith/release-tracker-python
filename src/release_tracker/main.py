import logging
import time

from fastapi import FastAPI, Request, Response, status
from sqlalchemy.exc.IntegrityError import IntegrityError

from .routers import projects

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Release Tracker API",
    description="A simple release tracker API",
    version="1.0.0",
)


@app.middleware("http")
async def my_middleware(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    logger.info(
        f"Response: {response.status_code} (Duration: {end_time - start_time:.2f}s)"
    )
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    logger.info(
        f"Response: {response.status_code} (Duration: {end_time - start_time:.2f}s)"
    )
    return response


# app.middleware("http")(my_middleware)


app.include_router(projects.router)


@app.exception_handler(IntegrityError)
def handle_integrity_error(request, exc: IntegrityError):
    logger.error("Integrity error occurred")
    return Response(
        content="Integrity error: Duplicate entry or constraint violation.",
        status_code=status.HTTP_409_CONFLICT,
    )


@app.get("/")
def root():
    return {"message": "Welcome to the Release Tracker API!"}
