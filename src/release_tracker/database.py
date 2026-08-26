from functools import lru_cache

from sqlalchemy.engine import Engine
from sqlmodel import create_engine

from release_tracker.config import get_settings


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()

    return create_engine(
        settings.database_url,
        echo=True,
    )
