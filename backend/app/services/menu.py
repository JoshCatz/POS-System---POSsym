from sqlalchemy import select
from app.schemas.menu import CreateMenuRequest, UpdateMenuRequest
from app.models.menu import MenuItem
from app.errors import NotFoundException, RedundantException
from app.config import settings

# Function to retrieve all menu items
async def get_all_menu_items(db, restaurant_id):
    result = await db.execute(select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)) # executes SQL command to get Menu Items associated with a given restaurant
    items = result.scalars().all() # pulls all the results

    return items

async def get_menu_item(db, item_id, restaurant_id):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id, MenuItem.restaurant_id == restaurant_id)) # executes SQL command to get single Menu Item associated with given restaurant
    item = result.scalar_one_or_none() # pulls one item or no items

    # if no items are found - raise a NotFoundException error
    if not item:
        raise NotFoundException(f"Menu item: {item_id}")

    return item 

async def create_menu_item(db, data: CreateMenuRequest):
    item = MenuItem(**data.model_dump(), restaurant_id=settings.RESTAURANT_ID) # creates an item modeling the schema created in CreateMenuRequest
    db.add(item) # adds the item to the database
    await db.commit() # commits the change
    await db.refresh(item) # reloads item from db so generated fields are populated

    return item

async def update_menu_item(db, item_id, restaurant_id, data: UpdateMenuRequest):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id, MenuItem.restaurant_id == restaurant_id)) # executes SQL command to get single Menu Item associated with given restaurant
    item = result.scalar_one_or_none() # pulls one item or no items

    # if no items are found - raise a NotFoundException error
    if not item:
        raise NotFoundException(f"Menu item {item_id}")
    
    # model_dump(exclude_none=True) returns only fields the client actually sent
    # setattr dynamically updates each field on the item
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(item, field, value)
    await db.commit() # commits the changes
    await db.refresh(item) # reloads item from db so generated fields are populated

    return item

async def eighty_six_item(db, item_id, restaurant_id):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id, MenuItem.restaurant_id == restaurant_id)) # executes SQL command to get single Menu Item associated with given restaurant
    item = result.scalar_one_or_none() # pulls one item or no items

    # if no items are found - raise a NotFoundException error
    if not item:
        raise NotFoundException(f"Menu item {item_id}")
    
    # if item is already 86 - raise a RedundantException error
    if item.is_active == False:
        raise RedundantException(f"Item already 86.")

    item.is_active = False # 86 item
    await db.commit() # commit the change
    await db.refresh(item) # reloads item from db so generated fields are populated
    return item
    
async def restore_item(db, item_id, restaurant_id):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id, MenuItem.restaurant_id == restaurant_id)) # executes SQL command to get single Menu Item associated with given restaurant
    item = result.scalar_one_or_none() # pulls one item or no items

    # if no items are found - raise a NotFoundException error
    if not item:
        raise NotFoundException(f"Menu item {item_id}")
    
    # if item is already active - raise a RedundantException error
    if item.is_active == True:
        raise RedundantException(f"Item already restored.")

    item.is_active = True # make item active
    await db.commit() # commit the change
    await db.refresh(item) # reloads item from db so generated fields are populated
    return item

