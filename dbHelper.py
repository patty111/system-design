from config import config
from typing import Generator
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
from sqlmodel import SQLModel, create_engine, Session

# engine = create_engine(f"sqlite:///./{config.db_name}", echo=config.db_echo)
engine = create_engine(f"sqlite:///./{config.db_name}", echo=False)
# session = sessionmaker(bind=engine, autocommit=False, autoflush=False, )

# Currently SQLite does not have an async driver, so unfortunately we can not use SqlAlchemy's async extension
def get_db() -> Generator:
    """create a db session"""
    with Session(engine) as session:
        yield session