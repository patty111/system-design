from sqlalchemy.orm import DeclarativeBase, Session, Any
from sqlalchemy import update, delete, select, text, insert
from typing import TypeVar, Type

T = TypeVar("T", bound="Base")  # for dynamic type hinting

class Base(DeclarativeBase):
    __abstract__ = True

    @classmethod
    def update(cls: Type[T], db: Session, model: Any) -> T:
        # stmt = update(cls).where(where).values(**kwargs)
        # db.execute(stmt)
        db.merge(model)
        db.commit()
        db.refresh(model)
        return model

    @classmethod
    def add(cls: Type[T], db: Session, model: Any) -> T:
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    @classmethod
    def delete(cls, db: Session, where):
        stmt = delete(cls).where(where)
        db.execute(stmt)
        db.commit()

    @classmethod
    def get(cls: Type[T], db: Session, where) -> T:
        stmt = select(cls).where(where)
        result = db.scalars(stmt)
        return result.one_or_none()