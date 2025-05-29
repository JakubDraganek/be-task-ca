from dataclasses import dataclass, field
from typing import List
from uuid import uuid4


@dataclass
class CartItem:
    """A value object representing an item in a cart."""
    item_id: str
    quantity: int
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class Cart:
    """A domain entity representing a user's shopping cart."""
    user_id: str
    id: str = field(default_factory=lambda: str(uuid4()))
    items: List[CartItem] = field(default_factory=list)

    def add_item(self, item_id: str, quantity: int) -> None:
        """Add an item to the cart."""
        # Check if item already exists
        for item in self.items:
            if item.item_id == item_id:
                item.quantity += quantity
                return
        
        # Add new item
        self.items.append(CartItem(item_id=item_id, quantity=quantity))

    def remove_item(self, item_id: str) -> None:
        """Remove an item from the cart."""
        self.items = [item for item in self.items if item.item_id != item_id]

    def update_item_quantity(self, item_id: str, quantity: int) -> None:
        """Update the quantity of an item in the cart."""
        for item in self.items:
            if item.item_id == item_id:
                item.quantity = quantity
                return
        raise ValueError(f"Item {item_id} not found in cart")

    def clear(self) -> None:
        """Remove all items from the cart."""
        self.items = [] 