import pytest
from sqlalchemy import text

from app.core.db import SessionLocal, engine


@pytest.fixture
def db_session():
    """Sesión de BD para tests de integración. No hace truncate — usa la BD real."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def db_engine():
    return engine


@pytest.fixture
def assert_db_alive(db_engine):
    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()
        assert result == 1
