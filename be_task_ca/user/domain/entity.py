from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class User:
    """Core User entity representing a user in the system."""
    id: UUID
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: Optional[str]

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
        ) 