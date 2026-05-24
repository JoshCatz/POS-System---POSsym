from pydantic import BaseModel

class POSLoginRequest(BaseModel):
    employee_id: int
    pin: str

class PortalLoginRequest(BaseModel):
    employee_id: int
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class TokenData(BaseModel):
    employee_id: int
    role: str
    restaurant_id: int
    auth_type: str