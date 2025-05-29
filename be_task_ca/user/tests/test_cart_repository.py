from uuid import uuid4
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from be_task_ca.database import Base
from be_task_ca.database.models import UserModel
from be_task_ca.user.domain.cart import Cart
from be_task_ca.user.infrastructure.cart_repository import PostgresCartRepository


@pytest.fixture
def test_db():
    """Create a test database engine and session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def test_user(test_db):
    """Create a test user."""
    user_id = str(uuid4())
    user = UserModel(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed_password",
    )
    test_db.add(user)
    test_db.commit()
    return user


@pytest.fixture
def cart_repository(test_db):
    """Create a cart repository instance."""
    return PostgresCartRepository(test_db)


@pytest.fixture
def test_items(test_db):
    """Create test items."""
    return [str(uuid4()) for _ in range(3)]


def test_create_cart(cart_repository, test_user):
    """Test creating a new cart."""
    cart = Cart(user_id=test_user.id)
    created_cart = cart_repository.create(cart)
    assert created_cart.id is not None
    assert created_cart.user_id == test_user.id
    assert len(created_cart.items) == 0


def test_get_cart_by_user_id(cart_repository, test_user):
    """Test retrieving a cart by user ID."""
    cart = Cart(user_id=test_user.id)
    created_cart = cart_repository.create(cart)
    retrieved_cart = cart_repository.get_by_user_id(test_user.id)
    assert retrieved_cart is not None
    assert retrieved_cart.id == created_cart.id
    assert retrieved_cart.user_id == test_user.id


def test_get_nonexistent_cart(cart_repository):
    """Test retrieving a cart that doesn't exist."""
    cart = cart_repository.get_by_user_id(str(uuid4()))
    assert cart is None


def test_update_cart(cart_repository, test_user, test_items):
    """Test updating a cart with items."""
    cart = Cart(user_id=test_user.id)
    created_cart = cart_repository.create(cart)
    created_cart.add_item(test_items[0], 2)
    updated_cart = cart_repository.update(created_cart)
    assert len(updated_cart.items) == 1
    assert updated_cart.items[0].item_id == test_items[0]
    assert updated_cart.items[0].quantity == 2


def test_delete_cart(cart_repository, test_user):
    """Test deleting a cart."""
    cart = Cart(user_id=test_user.id)
    created_cart = cart_repository.create(cart)
    cart_repository.delete(created_cart.id)
    retrieved_cart = cart_repository.get_by_user_id(test_user.id)
    assert retrieved_cart is None


def test_cart_operations_sequence(cart_repository, test_user, test_items):
    """Test a sequence of cart operations."""
    cart = Cart(user_id=test_user.id)
    created_cart = cart_repository.create(cart)
    created_cart.add_item(test_items[0], 2)
    created_cart.add_item(test_items[1], 1)
    updated_cart = cart_repository.update(created_cart)
    assert len(updated_cart.items) == 2
    assert any(item.item_id == test_items[0] and item.quantity == 2 for item in updated_cart.items)
    assert any(item.item_id == test_items[1] and item.quantity == 1 for item in updated_cart.items)
    updated_cart.update_item_quantity(test_items[0], 3)
    updated_cart = cart_repository.update(updated_cart)
    assert any(item.item_id == test_items[0] and item.quantity == 3 for item in updated_cart.items)
    updated_cart.remove_item(test_items[1])
    updated_cart = cart_repository.update(updated_cart)
    assert len(updated_cart.items) == 1
    assert updated_cart.items[0].item_id == test_items[0] 