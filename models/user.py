from sqlalchemy import String
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from config import config

class BaseUser(SQLModel):
    username: str = Field(default=None, nullable=False, max_length=50)

class User(BaseUser, table=True):
    __tablename__ = "users"
    username: str = Field(primary_key=True, default=None, max_length=50)
    password_hash: str = Field(default=None, nullable=False, max_length=32, min_length=32)
    salt: str = Field(default=None, nullable=False, max_length=20, min_length=20)
    created_at: Optional[str] = Field(default=datetime.now(), nullable=False)

class UserRegister(BaseUser):
    password: str = Field(default=None, nullable=False, min_length=8)