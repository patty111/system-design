from sqlalchemy import create_engine, MetaData, String, Integer, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase
from models.base import Base
from datetime import datetime

class Url(Base):
    __tablename__ = 'links'
    
    short_url: Mapped[str] = mapped_column(String(8), primary_key=True, unique=True, nullable=False)
    long_url: Mapped[str] = mapped_column(String, nullable=False)
    redirects: Mapped[int] = mapped_column(Integer, nullable=False ,default=0)
    create_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    expire_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by: Mapped[str] = mapped_column(String(50), default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def inactivate(self):
        self.is_active = False
        self.delete()

    def __repr__(self):
        return f"<Url(short_url='{self.short_url}', \
            long_url='{self.long_url}', \
            redirects={self.redirects}, \
            create_time='{self.create_time}', \
            expire_time='{self.expire_time}', \
            created_by='{self.created_by}', \
            is_active='{self.is_active}')>"