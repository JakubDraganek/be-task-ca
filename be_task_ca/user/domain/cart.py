from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class CartItem:
    """Represents an item in the shopping cart."""
    item_id: UUID
    quantity: int


@dataclass
class Cart:
    """Cart entity representing a user's shopping cart."""
    id: UUID
    user_id: UUID
    items: List[CartItem]

    @classmethod
    def create_new(cls, user_id: UUID) -> "Cart":
        """Factory method to create a new cart."""
        return cls(
            id=uuid4(),
            user_id=user_id,
            items=[],
        )

    def add_item(self, item_id: UUID, quantity: int) -> None:
        """Add an item to the cart."""
        # Check if item already exists in cart
        for cart_item in self.items:
            if cart_item.item_id == item_id:
                cart_item.quantity += quantity
                return

        # Add new item to cart
        self.items.append(CartItem(item_id=item_id, quantity=quantity))

    def remove_item(self, item_id: UUID) -> None:
        """Remove an item from the cart."""
        self.items = [item for item in self.items if item.item_id != item_id]

    def update_item_quantity(self, item_id: UUID, quantity: int) -> None:
        """Update the quantity of an item in the cart."""
        for cart_item in self.items:
            if cart_item.item_id == item_id:
                cart_item.quantity = quantity
                return
        raise ValueError(f"Item {item_id} not found in cart")

    def clear(self) -> None:
        """Remove all items from the cart."""
        self.items = [] 