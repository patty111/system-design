from sqlalchemy import String
from typing import Optional
from sqlmodel import Field, SQLModel
from config import config
from datetime import datetime, timedelta

class BaseUrl(SQLModel):
    short_url: str = Field(String(config.short_url_len), primary_key=True, unique=True, nullable=False)
    long_url: str = Field(nullable=False, unique=True)
    create_time: datetime = Field(default=datetime.now())
    expire_time: datetime = Field(nullable=False, default=datetime.now() + timedelta(days=30))
    created_by: Optional[str] = Field(default=None)

    def inactivate(self):
        # self.is_active = False
        # self.delete()
        pass
class Url(BaseUrl, table=True):
    __tablename__ = 'links'

    redirects: int = Field(default=0, nullable=False)
    last_redirect: datetime = Field(default=None)
    is_active: bool = Field(default=True, nullable=False)
    created_by: Optional[str] = Field(default=None, foreign_key="users.username")


class UrlCreate(BaseUrl):
    pass

class UrlRead(Url):
    """
    url info
    """


