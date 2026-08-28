from functools import lru_cache
from typing import Generator

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine

from release_tracker.config import get_settings


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()

    return create_engine(
        settings.database_url,
        echo=True,
    )


def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session
