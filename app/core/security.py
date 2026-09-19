from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta,timezone

password_hash = PasswordHash.recommended()
SECRET_KEY = "your_secret_key"

def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password:str, hashed_password:str):
    return password_hash.verify(password, hashed_password)



def create_access_token(user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
    "sub":str(user_id),
    "exp":expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
