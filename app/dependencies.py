import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import SECRET_KEY
from app.database import SessionLocal
from fastapi.security import HTTPBearer
from fastapi import Depends,HTTPException

from app.models.user import User


async def get_db():
    async with SessionLocal() as session:
        yield session



security = HTTPBearer()
async def get_current_user(
        token = Depends(security),
        db : AsyncSession = Depends(get_db)

):
    try:
        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=["HS256"],
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    user_id = int(payload["sub"])

    user = await db.get(User,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user




def require_role(required_role:str):
    async def role_cheker(current_user = Depends(get_current_user)):

        if current_user.role != required_role:
            raise HTTPException(status_code=403, detail="Incorrect role")

    return role_cheker