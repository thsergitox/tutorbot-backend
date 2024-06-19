from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from config import settings

Engine = create_engine(settings.DB_URL, pool_pre_ping = True)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = Engine)


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()