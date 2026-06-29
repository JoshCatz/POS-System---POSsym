from pydantic import BaseModel, Field

# Defines structure for all login requests sent to the POS interface
class POSLoginRequest(BaseModel):
    pin: str = Field(min_length=4, max_length=12)

# Defines structure for all login requests sent to the portal interface
class PortalLoginRequest(BaseModel):
    username: str = Field(min_length=4, max_length=48)
    password: str = Field(min_length=6, max_length=48)

# Defines structure for all systems to respond to successful login attempts
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    role: str

# Defines structure for token information to be transmitted
class TokenData(BaseModel):
    employee_id: int
    role: str
    restaurant_id: int
    auth_type: str