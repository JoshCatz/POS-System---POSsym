from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreateRequest, EmployeeResponse
from app.services.employee import set_employee_password, set_employee_pin, create_employee, get_employee

# Create route for /employees
router = APIRouter(prefix="/employees", tags=["employees"])

# Method to retrieve existing employee information by restaurant ID and employee ID
@router.get("", response_model=EmployeeResponse)
async def get_one_employee(restaurant_id:int, employee_id:int, db: AsyncSession = Depends(get_db)):
    return await get_employee(db, restaurant_id, employee_id)

# Method to create a new employee
@router.post("", response_model=EmployeeResponse)
async def create_employee_route(request: EmployeeCreateRequest, db: AsyncSession = Depends(get_db)):
    return await create_employee(db, request)