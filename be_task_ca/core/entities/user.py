from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class CartItem:
    """Represents an item in the user's shopping cart."""
    item_id: UUID
    quantity: int


@dataclass
class User:
    """Core User entity representing a user in the system."""
    id: UUID
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: Optional[str]
    cart_items: List[CartItem]

    @classmethod
    def create_new(
        cls,
        email: str,
        first_name: str,
        last_name: str,
        hashed_password: str,
        shipping_address: Optional[str] = None,
    ) -> "User":
        """Factory method to create a new user."""
        return cls(
            id=uuid4(),
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            shipping_address=shipping_address,
            cart_items=[],
        )

    def add_to_cart(self, item_id: UUID, quantity: int) -> None:
        """Add an item to the user's cart."""
        # Check if item already exists in cart
        for cart_item in self.cart_items:
            if cart_item.item_id == item_id:
                cart_item.quantity += quantity
                return

        # Add new item to cart
        self.cart_items.append(CartItem(item_id=item_id, quantity=quantity))

    def remove_from_cart(self, item_id: UUID) -> None:
        """Remove an item from the user's cart."""
        self.cart_items = [item for item in self.cart_items if item.item_id != item_id]

    def update_cart_item_quantity(self, item_id: UUID, quantity: int) -> None:
        """Update the quantity of an item in the cart."""
        for cart_item in self.cart_items:
            if cart_item.item_id == item_id:
                cart_item.quantity = quantity
                return
        raise ValueError(f"Item {item_id} not found in cart")

    def clear_cart(self) -> None:
        """Remove all items from the cart."""
        self.cart_items = [] 