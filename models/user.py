from sqlalchemy import String
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from config import config

# Solving circular imports for type Annotations: https://reurl.cc/xLx1MZ

class BaseUser(SQLModel):
    username: str = Field(default=None, nullable=False, max_length=50)
    links_created: Optional[int] = Field(default=0, nullable=False)


class User(BaseUser, table=True):
    __tablename__ = "users"
    username: str = Field(primary_key=True, default=None, max_length=50)
    password_hash: str = Field(default=None, nullable=False, max_length=60, min_length=60)
    salt: str = Field(default=None, nullable=False, max_length=20, min_length=20)
    created_at: Optional[str] = Field(default=datetime.now(), nullable=False)
    last_login: Optional[datetime] = Field(nullable=True)

    def toUserInfo(self) -> "UserInfo":
        from schemas.user_schema import UserInfo
            
        return UserInfo(
            username=self.username,
            links_created=self.links_created,
            last_login=self.last_login,
            created_at=self.created_at
        )