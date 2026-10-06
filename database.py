from sqlalchemy.ext.asyncio  import create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:////data/supportflow.db"

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass