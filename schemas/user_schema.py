from models.user import BaseUser
from sqlmodel import Field
from datetime import datetime
from typing import Optional

class UserRegister(BaseUser):
    password: str = Field(default=None, nullable=False, min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "username": "user",
                "password": "ji32k7au4a83"
            }
        }


class UserLogin(BaseUser):
    password: str = Field(default=None, nullable=False)

    class Config:
        schema_extra = {
            "example": {
                "username": "user",
                "password": "ithinkthisismypassword"
            }
        }


class UserInfo(BaseUser):
    created_at: datetime = Field(nullable=False)
    last_login: Optional[datetime] = Field(nullable=True)

    class Config:
        schema_extra = {
            "example": {
                "username": "user",
                "links_created": 2,
                "last_login": "2021-01-01 00:00:00"
            }
        }