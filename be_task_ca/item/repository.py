from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from be_task_ca.database.models import ItemModel
from .model import Item


def save_item(item: Item, db: Session) -> Item:
    """Save an item to the database."""
    item_model = ItemModel(
        id=str(item.id),
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )
    db.add(item_model)
    db.commit()
    return item


def get_all_items(db: Session) -> List[Item]:
    """Get all items from the database."""
    item_models = db.query(ItemModel).all()
    return [
        Item(
            id=UUID(item_model.id),
            name=item_model.name,
            description=item_model.description,
            price=item_model.price,
            quantity=item_model.quantity,
        )
        for item_model in item_models
    ]


def find_item_by_name(name: str, db: Session) -> Optional[Item]:
    """Find an item by name."""
    item_model = db.query(ItemModel).filter(ItemModel.name == name).first()
    if not item_model:
        return None
    return Item(
        id=UUID(item_model.id),
        name=item_model.name,
        description=item_model.description,
        price=item_model.price,
        quantity=item_model.quantity,
    )


def find_item_by_id(id: UUID, db: Session) -> Optional[Item]:
    """Find an item by ID."""
    item_model = db.query(ItemModel).filter(ItemModel.id == str(id)).first()
    if not item_model:
        return None
    return Item(
        id=UUID(item_model.id),
        name=item_model.name,
        description=item_model.description,
        price=item_model.price,
        quantity=item_model.quantity,
    )
