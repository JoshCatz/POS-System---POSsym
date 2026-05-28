from pydantic import BaseModel
from typing import Optional

class MenuItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None
    category_id: int
    category_name: Optional[str] = None
    active: bool

class CreateMenuRequest(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category_id: int
    restaurant_id: int

class UpdateMenuRequest(BaseModel):
    model_config = {"extra": "ignore"}

    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None