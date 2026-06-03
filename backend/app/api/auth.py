from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.employee import Employee
from app.schemas.auth import POSLoginRequest, PortalLoginRequest, LoginResponse
from app.services.auth import verify_password, create_token
from app.errors import UnauthorizedException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login/pos", response_model=LoginResponse)
async def pos_login(request: POSLoginRequest, db: AsyncSession = Depends(get_db)):

    # 1. Find employee by id
    result = await db.execute(select(Employee).where(Employee.id == request.employee_id))
    employee = result.scalar_one_or_none()

    # 2. Employee not found or pin wrong
    if not employee or not verify_password(request.pin, employee.pin_hash):
        raise UnauthorizedException()

    # 3. Create token
    token = create_token(
        employee_id=employee.id,
        restaurant_id=employee.restaurant_id,
        auth_type="pos"
    )

    return LoginResponse(access_token=token, token_type="bearer")


@router.post("/login/portal", response_model=LoginResponse)
async def portal_login(request: PortalLoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.id == request.employee_id))
    employee = result.scalar_one_or_none()

    if not employee or not verify_password(request.password, employee.password_hash):
        raise UnauthorizedException()

    token = create_token(
        employee_id=employee.id,
        restaurant_id=employee.restaurant_id,
        auth_type="portal"
    )

    return LoginResponse(access_token=token, token_type="bearer")