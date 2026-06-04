from pydantic import BaseModel, Field

class POSLoginRequest(BaseModel):
    restaurant_id: int
    pin: str = Field(min_length=4, max_length=12)

class PortalLoginRequest(BaseModel):
    username: str = Field(min_length=4, max_length=48)
    password: str = Field(min_length=6, max_length=48)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class TokenData(BaseModel):
    employee_id: int
    role: str
    restaurant_id: int
    auth_type: str