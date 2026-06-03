from pydantic import BaseModel

class POSLoginRequest(BaseModel):
    employee_id: int
    pin: str = Field(min_length=4, max_length=12)

class PortalLoginRequest(BaseModel):
    employee_id: int
    password: str = Field(min_length=8, max_length=128)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class TokenData(BaseModel):
    employee_id: int
    role: str
    restaurant_id: int
    auth_type: str