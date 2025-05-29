from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from .cart import Cart


class CartRepository(ABC):
    """Interface for cart persistence operations."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        """Get a user's cart (for viewing and modifying cart contents)."""
        pass

    @abstractmethod
    async def create(self, cart: Cart) -> Cart:
        """Create a new cart (when user first adds an item)."""
        pass

    @abstractmethod
    async def update(self, cart: Cart) -> Cart:
        """Update cart contents (when adding/removing items)."""
        pass

    @abstractmethod
    async def delete(self, cart_id: UUID) -> None:
        """Delete a cart by its ID."""
        pass 