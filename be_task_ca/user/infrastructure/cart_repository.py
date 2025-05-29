from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from be_task_ca.database.models import CartModel, CartItemModel
from be_task_ca.user.domain.cart import Cart, CartItem
from be_task_ca.user.domain.cart_repository import CartRepository


class PostgresCartRepository(CartRepository):
    """Synchronous implementation of the cart repository."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: str) -> Optional[Cart]:
        """Get a user's cart by their user ID."""
        stmt = select(CartModel).where(CartModel.user_id == user_id)
        result = self.session.execute(stmt)
        cart_model = result.scalar_one_or_none()

        if not cart_model:
            return None

        return self._to_domain(cart_model)

    def create(self, cart: Cart) -> Cart:
        """Create a new cart."""
        cart_model = CartModel(
            id=cart.id,
            user_id=cart.user_id,
        )
        self.session.add(cart_model)
        self.session.commit()
        self.session.refresh(cart_model)
        return self._to_domain(cart_model)

    def update(self, cart: Cart) -> Cart:
        """Update an existing cart."""
        stmt = select(CartModel).where(CartModel.id == cart.id)
        result = self.session.execute(stmt)
        cart_model = result.scalar_one_or_none()

        if not cart_model:
            raise ValueError(f"Cart {cart.id} not found")

        # Get existing items to preserve their IDs
        existing_items = {item.item_id: item for item in cart_model.items}

        # Update cart items
        new_items = []
        for item in cart.items:
            # If item exists, update it; otherwise create new
            if item.item_id in existing_items:
                existing_item = existing_items[item.item_id]
                existing_item.quantity = item.quantity
                new_items.append(existing_item)
            else:
                new_items.append(CartItemModel(
                    id=item.id,
                    cart_id=cart.id,
                    item_id=item.item_id,
                    quantity=item.quantity,
                ))

        cart_model.items = new_items
        self.session.commit()
        self.session.refresh(cart_model)
        return self._to_domain(cart_model)

    def delete(self, cart_id: str) -> None:
        """Delete a cart by its ID."""
        stmt = select(CartModel).where(CartModel.id == cart_id)
        result = self.session.execute(stmt)
        cart_model = result.scalar_one_or_none()

        if cart_model:
            self.session.delete(cart_model)
            self.session.commit()

    def _to_domain(self, cart_model: CartModel) -> Cart:
        """Convert a CartModel to a domain Cart entity."""
        return Cart(
            id=cart_model.id,
            user_id=cart_model.user_id,
            items=[
                CartItem(
                    id=item.id,
                    item_id=item.item_id,
                    quantity=item.quantity,
                )
                for item in cart_model.items
            ],
        ) 