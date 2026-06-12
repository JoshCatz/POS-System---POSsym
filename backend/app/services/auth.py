from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
import hashlib
import hmac
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings
from app.schemas.auth import TokenData
from app.errors import UnauthorizedException

# Creates a password hashing context for the application.
#
# CryptContext is a Passlib object that centralizes password hashing behavior.
# Instead of manually calling bcrypt throughout the codebase, we use this shared
# context anywhere we need to hash or verify passwords.
#
# schemes=["bcrypt"] tells Passlib to use bcrypt as the password hashing algorithm.
# bcrypt is designed for securely storing passwords because it is intentionally
# slow, which makes brute-force attacks harder.
#
# deprecated="auto" allows Passlib to manage deprecated hashing schemes
# automatically if we ever add or migrate hashing algorithms in the future.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Extracts the bearer token from the Authorization header of incoming requests.
# tokenUrl points Swagger's "Authorize" button at the login endpoint - it has
# no effect on runtime behavior, it's purely for the auto-generated docs.
bearer_scheme = HTTPBearer()

# Hashes a plain-text secret, such as a password or PIN, before storing it. 
# The original plain-text value should never be saved directly.
def hash_secret(secret: str) -> str:
    return pwd_context.hash(secret)

# Compares a plain-text secret against a previously hashed secret.
# Returns True if they match, otherwise False
def verify_secret(plain_secret: str, hashed_secret: str) -> bool:
    return pwd_context.verify(plain_secret, hashed_secret)

# Creates a signed JWT containing the employee's login/session information
# The token includes an expiration time so the session does not last forever.
def create_token(employee_id: int, restaurant_id: int, auth_type: str, name:str) -> str:
    payload = {
        "employee_id": employee_id,
        "restaurant_id": restaurant_id,
        "auth_type": auth_type,
        "name": name,
        "exp": datetime.now() + timedelta(minutes=settings.jwt_expire_minutes)
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

# Creates a secure lookup hash for a restaurant-specific PIN.
# This lets us search for a PIN without storing the raw PIN directly.
def create_pin_lookup_hash(restaurant_id: int, pin: str) -> str:
    message = f"{restaurant_id}:{pin}".encode("utf-8")
    secret = settings.pin_lookup_secret_key.encode("utf-8")

    return hmac.new(secret, message, hashlib.sha256,).hexdigest()

# Decodes and validates a JWT, then extracts the employee/session data from it. 
# Raises UnauthorizedException if the token is invalid or missing required fields.
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
    
# FastAPI dependency used on protected routes via Depends(get_current_user).
# Pulls the bearer token out of the request header (via oauth2_scheme),
# then decodes it into a TokenData object containing employee_id, restaurant_id,
# and auth_type. Raises UnauthorizedException if the token is missing or invalid.
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> TokenData:
    return decode_token(credentials.credentials)
