from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.user import UpdateUser
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user as create_user_service,
    update_user as update_user_service,
    delete_user as delete_user_service
    )

router = APIRouter()

# create a user and save in database
@router.post("/users")
async def create_user(
    name : str,
    email : str,
    db : AsyncSession = Depends(get_db)
):
    return await create_user_service(db, name, email)


# read all users
@router.get("/users")
async def get_users(db: AsyncSession= Depends(get_db)):

    return await get_all_users(db)
    # result = await get_all_users(db)
    # return result




@router.get("/users/{user_id}")
async def get_user(user_id : int, db: AsyncSession = Depends(get_db)):
    result = await get_user_by_id(db, user_id)
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
    user = await update_user_service(db, user_id, new_information)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# delete a user by id
@router.delete("/users/{user_id}")
async def delete_user(
    user_id : int,
    db : AsyncSession = Depends(get_db)
):
    user = await delete_user_service(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}

