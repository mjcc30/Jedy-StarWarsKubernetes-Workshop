from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool
import os

DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,
)


def get_session():
    # Create tables for the in-memory db if they don't exist
    # Note: In a real scenario with many tests, we might want to do this in a fixture.
    # But given the current setup where tests call create_all manually or rely on this,
    # ensuring tables exist for the session is key.
    # actually, test_users.py calls create_all manually.
    with Session(engine) as session:
        yield session
