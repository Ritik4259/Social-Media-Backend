from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from collections.abc import Generator
from .config import settings


SQL_ALCHEMY_DATABASE = (
    f"postgresql+psycopg://"
    f"{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(SQL_ALCHEMY_DATABASE, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()