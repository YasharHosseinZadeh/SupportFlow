from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models.user import User
from sqlalchemy import select
from app.schemas.user import UpdateUser

router = APIRouter()

# create a user and save in database
@router.post("/users")
async def create_user(
    name : str,
    email : str,
    db : AsyncSession = Depends(get_db)
):
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)


    return user


# read all users
@router.get("/users")
async def get_users(db: AsyncSession= Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()

    return users


@router.get("/users/{user_id}")
async def get_user(user_id : int, db: AsyncSession = Depends(get_db)):
    result = await db.get(User, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")


    return result



# update the user's information
@router.patch("/users/{user_id}")
async def update_user(
    user_id : int,
    new_information : UpdateUser,
    db : AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = new_information.name

    user.email = new_information.email

    await db.commit()

    await db.refresh(user)

    return user


# delete a user by id
@router.delete("/users/{user_id}")
async def delete_user(
    user_id : int,
    db : AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)

    await db.commit()

    return {"message": "User deleted"}

