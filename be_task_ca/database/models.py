from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from be_task_ca.database import Base


class UserModel(Base):
    """SQLAlchemy model for users."""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)  # UUID as string
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    shipping_address = Column(Text, nullable=True)

    cart = relationship("CartModel", back_populates="user", uselist=False)


class CartModel(Base):
    """SQLAlchemy model for shopping carts."""
    __tablename__ = "carts"

    id = Column(String(36), primary_key=True)  # UUID as string
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)

    user = relationship("UserModel", back_populates="cart")
    items = relationship("CartItemModel", back_populates="cart", cascade="all, delete-orphan")


class CartItemModel(Base):
    """SQLAlchemy model for items in a cart."""
    __tablename__ = "cart_items"

    id = Column(String(36), primary_key=True)  # UUID as string
    cart_id = Column(String(36), ForeignKey("carts.id"), nullable=False)
    item_id = Column(String(36), nullable=False)  # UUID as string
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("CartModel", back_populates="items")


class ItemModel(Base):
    """SQLAlchemy model for items."""
    __tablename__ = "items"

    id = Column(String(36), primary_key=True)  # UUID as string
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False) 