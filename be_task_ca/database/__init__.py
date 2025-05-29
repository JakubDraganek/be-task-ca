from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# Create PostgreSQL engine
engine = create_engine("postgresql://postgres:example@localhost:5432/postgres")

# Create all tables
from .models import UserModel, CartModel, CartItemModel  # noqa
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_db():
    """Get database session."""
    db = Session()
    try:
        yield db
    finally:
        db.close() 