from typing import List
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from be_task_ca.database import Base


class CartItemModel(Base):
    """SQLAlchemy model for cart items."""
    __tablename__ = "cart_items"

    cart_id: Mapped[UUID] = mapped_column(ForeignKey("carts.id"), primary_key=True)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"), primary_key=True)
    quantity: Mapped[int]


class CartModel(Base):
    """SQLAlchemy model for carts."""
    __tablename__ = "carts"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    items: Mapped[List[CartItemModel]] = relationship() 