from sqlalchemy import select
from app.schemas.restaurant import CreateRestaurantRequest
from app.models.restaurant import Restaurant
from app.errors import NotFoundException

# Function to retrieve a restaurant object from the database
async def get_restaurant(db, restaurant_id):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    items = result.scalars().all()

    return items

# Function to create a restaurant and store it within the database
async def create_restaurant(db, data: CreateRestaurantRequest):
    item = Restaurant(**data.model_dump())

    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item