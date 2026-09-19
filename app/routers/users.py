from typing import List
from app.models.user import User
from sqlalchemy import select
from app.core.security import verify_password,create_access_token
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user, require_role
from app.schemas.user import UpdateUser,UserResponse,UserLogin

from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user as create_user_service,
    update_user as update_user_service,
    delete_user as delete_user_service
    )

router = APIRouter()

# create a user and save in database
@router.post("/users",response_model=UserResponse)
async def create_user(
    name : str,
    email : str,
    password : str,
    db : AsyncSession = Depends(get_db)
):
    return await create_user_service(db, name, email, password)


# read all users
@router.get("/users")
async def get_users(
        db: AsyncSession= Depends(get_db),
        current_user = Depends(require_role("manager"))
):

    return current_user
    # result = await get_all_users(db)
    # return result




@router.get("/users/{user_id}",response_model=UserResponse)
async def get_user(user_id : int, db: AsyncSession = Depends(get_db)):
    result = await get_user_by_id(db, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    return result



# update the user's information
@router.patch("/users/{user_id}",response_model=UserResponse)
async def update_user(
    user_id : int,
    new_information : UpdateUser,
    db : AsyncSession = Depends(get_db)
):
    user = await update_user_service(db, user_id, new_information)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# delete a user by id
@router.delete("/users/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id : int,
    db : AsyncSession = Depends(get_db)
):
    user = await delete_user_service(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return


# Login endpoint
@router.post("/login")
async def login(user_info : UserLogin,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_info.email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    result = verify_password(user_info.password, user.password_hash)

    if result is False:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token(user.id)

    return token
