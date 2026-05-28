from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
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
    return await get_all_menu_items(db, restaurant_id)

@router.get("/{item_id}", response_model=MenuItemResponse)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await get_menu_item(db, item_id)

@router.post("/")
async def create_item(data: CreateMenuRequest, db: AsyncSession = Depends(get_db)):
    return await create_menu_item(db, data)

@router.put("/{item_id}")
async def update_item(data: UpdateMenuRequest, item_id: int, db: AsyncSession = Depends(get_db)):
    return await update_menu_item(db, item_id, data)

@router.post("/{item_id}/eighty-six")
async def eighty_six(item_id: int, db: AsyncSession = Depends(get_db)):

    return await eighty_six_item(db, item_id)

@router.post("/{item_id}/restore")
async def restore(item_id: int, db: AsyncSession = Depends(get_db)):
    return await restore_item(db, item_id)