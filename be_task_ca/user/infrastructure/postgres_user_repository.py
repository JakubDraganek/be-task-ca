from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..domain.entity import User
from ..domain.repository import UserRepository
from be_task_ca.database.models import UserModel


class PostgresUserRepository(UserRepository):
    """PostgreSQL implementation of UserRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        """Create a new user account."""
        user_model = UserModel(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address,
        )
        self.session.add(user_model)
        self.session.commit()
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email."""
        query = select(UserModel).where(UserModel.email == email)
        result = self.session.execute(query)
        user_model = result.scalar_one_or_none()

        if not user_model:
            return None

        return self._to_domain(user_model)

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by their ID."""
        query = select(UserModel).where(UserModel.id == str(user_id))
        result = self.session.execute(query)
        user_model = result.scalar_one_or_none()

        if not user_model:
            return None

        return self._to_domain(user_model)

    def update(self, user: User) -> User:
        """Update an existing user."""
        query = select(UserModel).where(UserModel.id == str(user.id))
        result = self.session.execute(query)
        user_model = result.scalar_one_or_none()

        if not user_model:
            raise ValueError(f"User with id {user.id} not found")

        user_model.email = user.email
        user_model.first_name = user.first_name
        user_model.last_name = user.last_name
        user_model.hashed_password = user.hashed_password
        user_model.shipping_address = user.shipping_address

        self.session.commit()
        return user

    def delete(self, user_id: UUID) -> None:
        """Delete a user by their ID."""
        query = select(UserModel).where(UserModel.id == str(user_id))
        result = self.session.execute(query)
        user_model = result.scalar_one_or_none()

        if not user_model:
            raise ValueError(f"User with id {user_id} not found")

        self.session.delete(user_model)
        self.session.commit()

    def list_all(self) -> List[User]:
        """List all users."""
        query = select(UserModel)
        result = self.session.execute(query)
        user_models = result.scalars().all()
        return [self._to_domain(user_model) for user_model in user_models]

    def _to_domain(self, user_model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity."""
        return User(
            id=UUID(user_model.id),
            email=user_model.email,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            hashed_password=user_model.hashed_password,
            shipping_address=user_model.shipping_address,
        ) 