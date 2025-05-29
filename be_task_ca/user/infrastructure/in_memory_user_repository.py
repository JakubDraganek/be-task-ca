from typing import Optional, List
from uuid import UUID

from ..domain.entity import User
from ..domain.repository import UserRepository


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository."""

    def __init__(self):
        self.users = {}

    def create(self, user: User) -> User:
        """Create a new user account."""
        self.users[str(user.id)] = user
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email."""
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by their ID."""
        return self.users.get(str(user_id))

    def update(self, user: User) -> User:
        """Update an existing user."""
        if str(user.id) not in self.users:
            raise ValueError(f"User with id {user.id} not found")
        self.users[str(user.id)] = user
        return user

    def delete(self, user_id: UUID) -> None:
        """Delete a user by their ID."""
        if str(user_id) not in self.users:
            raise ValueError(f"User with id {user_id} not found")
        del self.users[str(user_id)]

    def list_all(self) -> List[User]:
        """List all users."""
        return list(self.users.values()) 