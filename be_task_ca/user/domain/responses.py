from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID


@dataclass
class UserResponse:
    """Domain response model for user data."""
    id: UUID
    email: str
    first_name: str
    last_name: str
    shipping_address: Optional[str] = None


@dataclass
class UserListResponse:
    """Domain response model for list of users."""
    users: List[UserResponse] 