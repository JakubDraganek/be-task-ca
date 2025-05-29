from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from be_task_ca.database import get_db
from be_task_ca.user.infrastructure.postgres_user_repository import PostgresUserRepository
from be_task_ca.user.schema import (
    CreateUserRequest,
    CreateUserResponse,
)
from be_task_ca.user.usecases import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_user,
    delete_user,
    list_users,
)


user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


def get_user_repository(db: Session = Depends(get_db)) -> PostgresUserRepository:
    """Get user repository instance."""
    return PostgresUserRepository(db)


@user_router.post("/", response_model=CreateUserResponse)
def create_user_endpoint(
    user: CreateUserRequest,
    user_repository: PostgresUserRepository = Depends(get_user_repository),
) -> CreateUserResponse:
    """Create a new user."""
    try:
        user_response = create_user(user, user_repository)
        return CreateUserResponse(
            id=user_response.id,
            email=user_response.email,
            first_name=user_response.first_name,
            last_name=user_response.last_name,
            shipping_address=user_response.shipping_address,
        )
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/email/{email}", response_model=CreateUserResponse)
def get_user_by_email_endpoint(
    email: str,
    user_repository: PostgresUserRepository = Depends(get_user_repository),
) -> CreateUserResponse:
    """Get user by email."""
    try:
        user_response = get_user_by_email(email, user_repository)
        return CreateUserResponse(
            id=user_response.id,
            email=user_response.email,
            first_name=user_response.first_name,
            last_name=user_response.last_name,
            shipping_address=user_response.shipping_address,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.get("/{user_id}", response_model=CreateUserResponse)
def get_user_by_id_endpoint(
    user_id: str,
    user_repository: PostgresUserRepository = Depends(get_user_repository),
) -> CreateUserResponse:
    """Get user by ID."""
    try:
        user_response = get_user_by_id(user_id, user_repository)
        return CreateUserResponse(
            id=user_response.id,
            email=user_response.email,
            first_name=user_response.first_name,
            last_name=user_response.last_name,
            shipping_address=user_response.shipping_address,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.put("/{user_id}", response_model=CreateUserResponse)
def update_user_endpoint(
    user_id: str,
    user: CreateUserRequest,
    user_repository: PostgresUserRepository = Depends(get_user_repository),
) -> CreateUserResponse:
    """Update user information."""
    try:
        user_response = update_user(user_id, user, user_repository)
        return CreateUserResponse(
            id=user_response.id,
            email=user_response.email,
            first_name=user_response.first_name,
            last_name=user_response.last_name,
            shipping_address=user_response.shipping_address,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.delete("/{user_id}")
def delete_user_endpoint(
    user_id: str,
    user_repository: PostgresUserRepository = Depends(get_user_repository),
) -> None:
    """Delete a user."""
    try:
        delete_user(user_id, user_repository)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.get("/", response_model=list[CreateUserResponse])
def list_users_endpoint(
    user_repository: PostgresUserRepository = Depends(get_user_repository),
) -> list[CreateUserResponse]:
    """List all users."""
    user_list = list_users(user_repository)
    return [
        CreateUserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            shipping_address=user.shipping_address,
        )
        for user in user_list.users
    ]
