from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreateRequest, EmployeeResponse
from app.services.employee import set_employee_password, set_employee_pin, create_employee


router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse)
async def create_employee_route(request: EmployeeCreateRequest,db: AsyncSession = Depends(get_db)):
    return await create_employee(db, request)