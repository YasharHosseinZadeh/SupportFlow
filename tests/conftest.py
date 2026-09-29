import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.models.user import User
from app.models.ticket import Ticket
from app.core.security import hash_password

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_supportflow.db"

test_engine = create_async_engine(TEST_DATABASE_URL)


TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False
)

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    async  with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def test_user():
    async with TestSessionLocal() as session:
        user = User(
            name="Test",
            email="Test@example.com",
            password_hash="fake_hash",
            role="customer"
        )
        session.add(user)

        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture
async def test_user_2():
    async with TestSessionLocal() as session:
        user = User(
            name="test2",
            email="test2@example.com",
            password_hash="fake_hash",
            role="customer"
        )
        session.add(user)

        await session.commit()
        await session.refresh(user)
        return user



@pytest_asyncio.fixture
async def test_manager():
    async with TestSessionLocal() as session:

        user = User(
        name="Yashar",
        email="Yashar@example.com",
        password_hash="fake_hash",
        role="manager"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture
async def test_ticket(test_user):
    async with TestSessionLocal() as session:
        ticket = Ticket(
        title = "Test Ticket" ,
        description = "This is a test ticket" ,
        customer_id = test_user.id
        )
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)
        return ticket


@pytest_asyncio.fixture
async def login_user():
    async with TestSessionLocal() as session:
        user = User(
            name="Test",
            email="Test@example.com",
            password_hash = hash_password("Test1234"),
            role = "customer"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user