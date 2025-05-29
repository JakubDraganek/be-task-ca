from .database import engine, Base

# just importing all the models is enough to have them created
# flake8: noqa
from .database.models import UserModel, CartModel, CartItemModel


def create_db_schema():
    Base.metadata.create_all(bind=engine)
