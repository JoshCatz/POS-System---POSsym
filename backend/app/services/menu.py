from sqlalchemy import select
from app.schemas.menu import CreateMenuRequest, UpdateMenuRequest
from app.models.menu import Menu
from app.errors import NotFoundException, RedundantException

async def get_all_menu_items(db, restaurant_id):
    result = await db.execute(select(Menu).where(Menu.restaurant_id == restaurant_id))
    items = result.scalars().all()

    return items

async def get_menu_item(db, item_id):
    result = await db.execute(select(Menu).where(Menu.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise NotFoundException(f"Menu item: {item_id}")

    return item

async def create_menu_item(db, data: CreateMenuRequest):
    item = Menu(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item

async def update_menu_item(db, item_id, data: UpdateMenuRequest):
    result = await db.execute(select(Menu).where(Menu.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise NotFoundException(f"Menu item {item_id}")
    
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)

    return item

async def eighty_six_item(db, item_id):
    result = await db.execute(select(Menu).where(Menu.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise NotFoundException(f"Menu item {item_id}")
    
    if item.active == False:
        raise RedundantException(f"Item already 86.")

    item.active = False
    await db.commit()
    await db.refresh(item)
    return item
    
async def restore_item(db, item_id):
    result = await db.execute(select(Menu).where(Menu.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise NotFoundException(f"Menu item {item_id}")
    
    if item.active == True:
        raise RedundantException(f"Item already restored.")

    item.active = True
    await db.commit()
    await db.refresh(item)
    return item

