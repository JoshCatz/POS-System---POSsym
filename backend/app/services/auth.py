from passlib.context import CryptContext
from jose import jwt, JWTError
import os
from datetime import datetime, timedelta
from app.schemas.auth import TokenData
from app.errors import UnauthorizedException

SECRET_KEY = os.getenv("JWT_SECRET")
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 480))

myctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
   return  myctx.hash(password)

def verify_password(password:str, hashed:str) -> bool:
   return myctx.verify(password, hashed)

def create_token(employee_id: int, role: str, restaurant_id: int, auth_type: str) -> str:
    payload = {
        "employee_id": employee_id,
        "role": role,
        "restaurant_id": restaurant_id,
        "auth_type": auth_type,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        employee_id = payload.get("employee_id")
        role = payload.get("role")
        restaurant_id = payload.get("restaurant_id")
        return TokenData(
            employee_id=employee_id,
            role=role,
            restaurant_id=restaurant_id
        )
    except JWTError:
        raise UnauthorizedException()
