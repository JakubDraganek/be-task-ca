import uuid
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from be_task_ca.database import Base
from be_task_ca.user.domain.entity import User
from be_task_ca.user.infrastructure.postgres_user_repository import PostgresUserRepository


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    # Use in-memory SQLite for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def test_session(test_engine) -> Generator:
    """Create a test database session."""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def user_repository(test_session) -> Generator:
    """Create a user repository instance."""
    repo = PostgresUserRepository(test_session)
    yield repo


@pytest.fixture
def test_user(user_repository) -> Generator:
    """Create a test user for use in test cases."""
    user = User.create_new(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed_password",
        shipping_address="123 Test St"
    )
    created_user = user_repository.create(user)
    yield created_user 