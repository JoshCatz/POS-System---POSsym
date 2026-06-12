from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.restaurant import CreateRestaurantRequest, RestaurantResponse
from app.services.restaurant import (
    get_restaurant,
    create_restaurant
)

# Creates route for /restaurant functions
router = APIRouter(prefix="/restaurant", tags=["restaurant"])

# Retrieve existing restaurant information by restaurant ID
@router.get("/")
async def get_restaurant_info(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await get_restaurant(db, restaurant_id)

# Create new restaurant
@router.post("/")
async def create_new_restaurant(data: CreateRestaurantRequest, db: AsyncSession = Depends(get_db)):
    return await create_restaurant(db, data)

