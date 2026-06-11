from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
import hashlib
import hmac

from app.config import settings
from app.schemas.auth import TokenData
from app.errors import UnauthorizedException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_secret(secret: str) -> str:
    return pwd_context.hash(secret)

def verify_secret(plain_secret: str, hashed_secret: str) -> bool:
    return pwd_context.verify(plain_secret, hashed_secret)

def create_token(employee_id: int, restaurant_id: int, auth_type: str, name:str) -> str:
    payload = {
        "employee_id": employee_id,
        "restaurant_id": restaurant_id,
        "auth_type": auth_type,
        "name": name,
        "exp": datetime.now() + timedelta(minutes=settings.jwt_expire_minutes)
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def create_pin_lookup_hash(restaurant_id: int, pin: str) -> str:
    message = f"{restaurant_id}:{pin}".encode("utf-8")
    secret = settings.pin_lookup_secret_key.encode("utf-8")

    return hmac.new(secret, message, hashlib.sha256,).hexdigest()

def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        employee_id = payload.get("employee_id")
        restaurant_id = payload.get("restaurant_id")
        auth_type = payload.get("auth_type")

        if employee_id is None or restaurant_id is None or auth_type is None:
            raise UnauthorizedException()

        return TokenData(
            employee_id=employee_id,
            restaurant_id=restaurant_id,
            auth_type=auth_type,
        )

    except JWTError:
        raise UnauthorizedException()
