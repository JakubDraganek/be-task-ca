from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.cart import Cart, CartItem
from ..domain.cart_repository import CartRepository
from ..model import CartItem as CartItemModel, User as UserModel


class PostgresCartRepository(CartRepository):
    """PostgreSQL implementation of CartRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        """Get a user's cart."""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()

        if not user_model:
            return None

        return self._to_domain(user_model)

    async def create(self, cart: Cart) -> Cart:
        """Create a new cart by adding items to user's cart."""
        # Get user
        query = select(UserModel).where(UserModel.id == cart.user_id)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()

        if not user_model:
            raise ValueError(f"User {cart.user_id} not found")

        # Add cart items
        for item in cart.items:
            cart_item = CartItemModel(
                user_id=cart.user_id,
                item_id=item.item_id,
                quantity=item.quantity,
            )
            self.session.add(cart_item)

        await self.session.commit()
        return cart

    async def update(self, cart: Cart) -> Cart:
        """Update cart contents."""
        # Get user
        query = select(UserModel).where(UserModel.id == cart.user_id)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()

        if not user_model:
            raise ValueError(f"User {cart.user_id} not found")

        # Remove existing items
        await self.session.execute(
            select(CartItemModel).where(CartItemModel.user_id == cart.user_id)
        )
        for item in user_model.cart_items:
            await self.session.delete(item)

        # Add new items
        for item in cart.items:
            cart_item = CartItemModel(
                user_id=cart.user_id,
                item_id=item.item_id,
                quantity=item.quantity,
            )
            self.session.add(cart_item)

        await self.session.commit()
        return cart

    def _to_domain(self, user_model: UserModel) -> Cart:
        """Convert SQLAlchemy model to domain entity."""
        return Cart(
            id=user_model.id,  # Using user_id as cart_id since they're 1:1
            user_id=user_model.id,
            items=[
                CartItem(
                    item_id=item.item_id,
                    quantity=item.quantity,
                )
                for item in user_model.cart_items
            ],
        ) 