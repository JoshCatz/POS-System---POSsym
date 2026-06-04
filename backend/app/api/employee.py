from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreateRequest, EmployeeResponse
from app.services.employee import set_employee_password, set_employee_pin


router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse)
async def create_employee(
    request: EmployeeCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    employee = Employee(
        restaurant_id=request.restaurant_id,
        name=request.name,
        username=request.username,
        is_active=True,
    )

    if request.pin:
        await set_employee_pin(db, employee, request.pin)

    if request.password:
        set_employee_password(employee, request.password)

    db.add(employee)
    await db.commit()
    await db.refresh(employee)

    return employee