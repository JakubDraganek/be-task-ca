import pytest
from uuid import UUID

from be_task_ca.user.domain.entity import User
from be_task_ca.user.usecases import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_user,
    delete_user,
    list_users,
)
from be_task_ca.user.schema import CreateUserRequest
from be_task_ca.user.infrastructure.in_memory_user_repository import InMemoryUserRepository


@pytest.fixture
def user_repository():
    """Create an in-memory user repository instance."""
    return InMemoryUserRepository()


@pytest.fixture
def test_user(user_repository):
    """Create a test user for use in test cases."""
    request = CreateUserRequest(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="password123",
        shipping_address="123 Test St"
    )
    return create_user(request, user_repository)


def test_create_user(user_repository):
    """Test creating a new user."""
    request = CreateUserRequest(
        email="new@example.com",
        first_name="New",
        last_name="User",
        password="password123",
        shipping_address="456 New St"
    )
    response = create_user(request, user_repository)
    assert response.email == "new@example.com"
    assert response.first_name == "New"
    assert response.last_name == "User"
    assert response.shipping_address == "456 New St"


def test_create_user_duplicate_email(user_repository, test_user):
    """Test creating a user with duplicate email."""
    request = CreateUserRequest(
        email="test@example.com",  # Same email as test_user
        first_name="Another",
        last_name="User",
        password="password123",
        shipping_address="789 Another St"
    )
    with pytest.raises(ValueError) as exc_info:
        create_user(request, user_repository)
    assert "already exists" in str(exc_info.value)


def test_get_user_by_email(user_repository, test_user):
    """Test getting a user by email."""
    response = get_user_by_email("test@example.com", user_repository)
    assert response.id == test_user.id
    assert response.email == "test@example.com"


def test_get_user_by_email_not_found(user_repository):
    """Test getting a non-existent user by email."""
    with pytest.raises(ValueError) as exc_info:
        get_user_by_email("nonexistent@example.com", user_repository)
    assert "not found" in str(exc_info.value)


def test_get_user_by_id(user_repository, test_user):
    """Test getting a user by ID."""
    response = get_user_by_id(str(test_user.id), user_repository)
    assert response.id == test_user.id
    assert response.email == "test@example.com"


def test_get_user_by_id_not_found(user_repository):
    """Test getting a non-existent user by ID."""
    with pytest.raises(ValueError) as exc_info:
        get_user_by_id("nonexistent-id", user_repository)
    assert "not found" in str(exc_info.value)


def test_update_user(user_repository, test_user):
    """Test updating a user."""
    request = CreateUserRequest(
        email="updated@example.com",
        first_name="Updated",
        last_name="User",
        password="newpassword123",
        shipping_address="789 Updated St"
    )
    response = update_user(str(test_user.id), request, user_repository)
    assert response.email == "updated@example.com"
    assert response.first_name == "Updated"
    assert response.last_name == "User"
    assert response.shipping_address == "789 Updated St"


def test_update_user_not_found(user_repository):
    """Test updating a non-existent user."""
    request = CreateUserRequest(
        email="updated@example.com",
        first_name="Updated",
        last_name="User",
        password="newpassword123",
        shipping_address="789 Updated St"
    )
    with pytest.raises(ValueError) as exc_info:
        update_user("nonexistent-id", request, user_repository)
    assert "not found" in str(exc_info.value)


def test_delete_user(user_repository, test_user):
    """Test deleting a user."""
    delete_user(str(test_user.id), user_repository)
    with pytest.raises(ValueError) as exc_info:
        get_user_by_id(str(test_user.id), user_repository)
    assert "not found" in str(exc_info.value)


def test_delete_user_not_found(user_repository):
    """Test deleting a non-existent user."""
    with pytest.raises(ValueError) as exc_info:
        delete_user("nonexistent-id", user_repository)
    assert "not found" in str(exc_info.value)


def test_list_users(user_repository, test_user):
    """Test listing all users."""
    # Create another user
    request = CreateUserRequest(
        email="another@example.com",
        first_name="Another",
        last_name="User",
        password="password123",
        shipping_address="456 Another St"
    )
    create_user(request, user_repository)

    # List all users
    response = list_users(user_repository)
    assert len(response.users) == 2
    emails = {user.email for user in response.users}
    assert emails == {"test@example.com", "another@example.com"} 