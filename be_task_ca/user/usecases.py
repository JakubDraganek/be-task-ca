import hashlib
from typing import List
from uuid import UUID

from .domain.entity import User
from .domain.repository import UserRepository
from .domain.responses import UserResponse, UserListResponse
from .schema import CreateUserRequest


def hash_password(password: str) -> str:
    """Hash a password using SHA-512."""
    return hashlib.sha512(password.encode("UTF-8")).hexdigest()


def create_user(create_user_request: CreateUserRequest, user_repository: UserRepository) -> UserResponse:
    """Create a new user account."""
    # Check if user with this email already exists
    existing_user = user_repository.get_by_email(create_user_request.email)
    if existing_user is not None:
        raise ValueError("A user with this email address already exists")

    # Create new user with hashed password
    new_user = User.create_new(
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=hash_password(create_user_request.password),
        shipping_address=create_user_request.shipping_address,
    )

    # Save user through repository
    created_user = user_repository.create(new_user)

    # Return response
    return UserResponse(
        id=created_user.id,
        first_name=created_user.first_name,
        last_name=created_user.last_name,
        email=created_user.email,
        shipping_address=created_user.shipping_address,
    )


def get_user_by_email(email: str, user_repository: UserRepository) -> UserResponse:
    """Get user by email."""
    user = user_repository.get_by_email(email)
    if user is None:
        raise ValueError("User not found")

    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        shipping_address=user.shipping_address,
    )


def get_user_by_id(user_id: str, user_repository: UserRepository) -> UserResponse:
    """Get user by ID."""
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise ValueError("User not found")

    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        shipping_address=user.shipping_address,
    )


def update_user(user_id: str, update_data: CreateUserRequest, user_repository: UserRepository) -> UserResponse:
    """Update user information."""
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise ValueError("User not found")

    # Update user fields
    user.first_name = update_data.first_name
    user.last_name = update_data.last_name
    user.email = update_data.email
    user.shipping_address = update_data.shipping_address
    if update_data.password:
        user.hashed_password = hash_password(update_data.password)

    updated_user = user_repository.update(user)

    return UserResponse(
        id=updated_user.id,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        email=updated_user.email,
        shipping_address=updated_user.shipping_address,
    )


def delete_user(user_id: str, user_repository: UserRepository) -> None:
    """Delete a user."""
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise ValueError("User not found")

    user_repository.delete(user_id)


def list_users(user_repository: UserRepository) -> UserListResponse:
    """List all users."""
    users = user_repository.list_all()
    return UserListResponse(
        users=[
            UserResponse(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                shipping_address=user.shipping_address,
            )
            for user in users
        ]
    )
