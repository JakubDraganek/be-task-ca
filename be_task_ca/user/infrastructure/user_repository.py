from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.entity import User
from ..domain.repository import UserRepository
from ..model import User as UserModel


class PostgresUserRepository(UserRepository):
    """PostgreSQL implementation of UserRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        """Create a new user account."""
        user_model = UserModel(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address,
        )
        self.session.add(user_model)
        await self.session.commit()
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email."""
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()

        if not user_model:
            return None

        return self._to_domain(user_model)

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by their ID."""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()

        if not user_model:
            return None

        return self._to_domain(user_model)

    def _to_domain(self, user_model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity."""
        return User(
            id=user_model.id,
            email=user_model.email,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            hashed_password=user_model.hashed_password,
            shipping_address=user_model.shipping_address,
        ) 