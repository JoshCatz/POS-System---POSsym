from pydantic import BaseModel
from typing import Optional

class RestaurantResponse(BaseModel):
    id: int
    name: str
    company: str
    address: str
    city: str
    state: str
    country: str

class CreateRestaurantRequest(BaseModel):
    id: int
    name: str
    company: str
    address: str
    city: str
    state: str
    country: str