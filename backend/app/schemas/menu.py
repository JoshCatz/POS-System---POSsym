from pydantic import BaseModel
from typing import Optional

# Defines structure of data that should be returned from api for retrieving menu item(s)
class MenuItemResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    price: float
    description: Optional[str] = None
    category_id: int
    category_name: Optional[str] = None
    is_active: bool

# Defines structure of data that should be sent to api for creating a menu item
class CreateMenuRequest(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category_id: int
    restaurant_id: int

# Defines structure of data that should be sent to api for updating existing menu item(s)
class UpdateMenuRequest(BaseModel):
    model_config = {"extra": "ignore"}

    # each attribute is optional - not everything needs to be updated
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None