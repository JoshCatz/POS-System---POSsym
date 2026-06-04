from pydantic import BaseModel, Field


class EmployeeCreateRequest(BaseModel):
    restaurant_id: int
    name: str = Field(min_length=1, max_length=255)
    username: str | None = Field(default=None, min_length=4, max_length=48)
    pin: str | None = Field(default=None, min_length=4, max_length=12)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class EmployeeResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    username: str | None
    is_active: bool

    model_config = {
        "from_attributes": True
    }