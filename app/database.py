from sqlalchemy.ext.asyncio  import create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./supportflow.db"

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass