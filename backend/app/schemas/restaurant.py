from pydantic import BaseModel
from typing import Optional

# Defines structure for sending POST /restaurants requests
class CreateRestaurantRequest(BaseModel):
    id: int
    name: str
    company: str
    address: str
    city: str
    state: str
    country: str

# Defines structure for system to respond to GET /restaurants requests
class RestaurantResponse(BaseModel):
    id: int
    name: str
    company: str
    address: str
    city: str
    state: str
    country: str