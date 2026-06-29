from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreateRequest, EmployeeResponse
from app.services.employee import create_employee, get_employee, get_all_employees
from app.services.auth import get_current_user
from app.schemas.auth import TokenData

# Create route for /employees
router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("", response_model=list[EmployeeResponse])
async def get_employees(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await get_all_employees(db, restaurant_id)

# Method to retrieve existing employee information by restaurant ID and employee ID
@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_one_employee(employee_id: int, db: AsyncSession = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    return await get_employee(db, employee_id, current_user.restaurant_id)

# Method to create a new employee
@router.post("", response_model=EmployeeResponse)
async def create_employee_route(request: EmployeeCreateRequest, db: AsyncSession = Depends(get_db)):
    return await create_employee(db, request)