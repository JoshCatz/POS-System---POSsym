from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.rbac import AssignRoleRequest, RoleResponse
from app.services.rbac import (
    get_all_roles,
    get_employee_roles,
    assign_role,
    remove_role
)
from app.schemas.auth import TokenData
from app.services.auth import get_current_user

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=list[RoleResponse]) 
async def get_roles(db: AsyncSession = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    return await get_all_roles(db) # async call to get_all_roles

@router.get("/employees/{employee_id}", response_model=list[RoleResponse])
async def employee_roles(employee_id: int, db: AsyncSession = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    return await get_employee_roles(db, employee_id, current_user.restaurant_id) # async call to get_employee_roles

@router.post("/employees/{employee_id}")
async def create_role(employee_id: int, data: AssignRoleRequest, db: AsyncSession = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    return await assign_role(db, data, employee_id, current_user.restaurant_id) # async call to assign_role

@router.delete("/employees/{employee_id}/{role_id}")
async def delete_role(employee_id: int, role_id: int, db: AsyncSession = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    return await remove_role(db, role_id, employee_id, current_user.restaurant_id) # async call to remove_role
