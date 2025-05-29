from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Item:
    """Domain model for items."""
    id: UUID
    name: str
    description: str
    price: float
    quantity: int

    @classmethod
    def create_new(cls, name: str, description: str, price: float, quantity: int) -> "Item":
        """Create a new item with a generated UUID."""
        return cls(
            id=uuid4(),
            name=name,
            description=description,
            price=price,
            quantity=quantity,
        )
