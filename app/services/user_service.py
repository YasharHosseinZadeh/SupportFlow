from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select
from app.schemas.user import UpdateUser


async def get_all_users(db: AsyncSession):
    users = await db.execute(select(User))
    return users.scalars().all()



async def get_user_by_id(db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    return user


async def create_user(db: AsyncSession,name: str, email: str):
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: int,new_information: UpdateUser):
    user = await db.get(User, user_id)
    if user is None:
        return None
    user.name = new_information.name
    user.email = new_information.email
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    if user is None:
        return None
    await db.delete(user)
    await db.commit()
    return user