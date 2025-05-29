from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from .entity import User


class UserRepository(ABC):
    """Interface for user persistence operations."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user account."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email (for login/authentication)."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by their ID (for cart operations)."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user."""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """Delete a user by their ID."""
        pass

    @abstractmethod
    async def list_all(self) -> List[User]:
        """List all users."""
        pass 