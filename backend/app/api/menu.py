from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.menu import MenuItemResponse, CreateMenuRequest, UpdateMenuRequest
from app.services.menu import (
    get_all_menu_items,
    get_menu_item,
    create_menu_item,
    update_menu_item,
    eighty_six_item,
    restore_item
)

router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/") 
async def get_menu(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await get_all_menu_items(db, restaurant_id) # async call to get_all_menu_items 

@router.get("/{item_id}", response_model=MenuItemResponse)
async def read_item(item_id: int, restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await get_menu_item(db, item_id, restaurant_id) # async call to get_menu_item

@router.post("/")
async def create_item(data: CreateMenuRequest, db: AsyncSession = Depends(get_db)):
    return await create_menu_item(db, data) # async call to create_menu_items

@router.put("/{item_id}")
async def update_item(data: UpdateMenuRequest, item_id: int, restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await update_menu_item(db, item_id, restaurant_id, data) # async call to update_menu_item

@router.post("/{item_id}/eighty-six")
async def eighty_six(item_id: int, restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await eighty_six_item(db, item_id, restaurant_id) # async call to eighty_six_item

@router.post("/{item_id}/restore")
async def restore(item_id: int, restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await restore_item(db, item_id, restaurant_id) # async call to restore_item