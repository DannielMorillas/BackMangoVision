import pytest
from sqlalchemy import text

from app.core.db import SessionLocal, engine
from app.core.security import hash_password
from app.models import User, UserRole


@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def db_engine():
    return engine


@pytest.fixture
def clean_users_table(db_session):
    """Trunca users (CASCADE) antes y después del test que la solicita."""
    db_session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    db_session.commit()
    yield
    db_session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    db_session.commit()


@pytest.fixture
def make_user(db_session, clean_users_table):
    """Factory para crear usuarios persistidos."""
    created: list[User] = []

    def _factory(
        *,
        email: str = "agronomo@example.com",
        password: str = "ClaveSegura123",
        role: UserRole = UserRole.AGRONOMIST,
        is_active: bool = True,
        must_change_password: bool = False,
        first_name: str = "Juan",
        last_name: str = "Perez",
    ) -> User:
        user = User(
            email=email.lower(),
            password_hash=hash_password(password),
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=is_active,
            must_change_password=must_change_password,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        created.append(user)
        return user

    return _factory
