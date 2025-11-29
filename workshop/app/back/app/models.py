from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class EntityImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entity_name: str = Field(index=True, unique=True)
    image_url: str
    description: Optional[str] = None


class ChatHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    character_name: str
    message: str
    response: str
    timestamp: Optional[str] = None
