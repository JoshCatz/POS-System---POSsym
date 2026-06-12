from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.employee import Employee
from app.models.restaurant import Restaurant
from app.schemas.auth import POSLoginRequest, PortalLoginRequest, LoginResponse
from app.services.auth import verify_secret, create_token, create_pin_lookup_hash
from app.errors import UnauthorizedException

# Create route for /auth which will be used for all logins
router = APIRouter(prefix="/auth", tags=["auth"])

# Method for users to login to the POS system
@router.post("/login/pos", response_model=LoginResponse)
async def pos_login(request: POSLoginRequest, db: AsyncSession = Depends(get_db)):

    # 1. Generate lookup hash
    pin_lookup_hash = create_pin_lookup_hash(restaurant_id = request.restaurant_id, pin=request.pin)

    # 2. Find employee by lookup hash
    result = await db.execute(select(Employee).where(Employee.restaurant_id == request.restaurant_id, Employee.pin_lookup_hash == pin_lookup_hash, Employee.is_active == True))
    employee = result.scalar_one_or_none()

    # 3. Employee not found
    if not employee or not employee.is_active:
        raise UnauthorizedException()
        # Figure out how to print on front-end message "Employee not found."

    # 3. Employee does not have a set pin
    if not employee.pin_hash:
        raise UnauthorizedException()
        # Figure out how to print on front-end message like "Has the user configured their pin yet?"

    # 4. Given pin is incorrect
    if not verify_secret(request.pin, employee.pin_hash):
        raise UnauthorizedException()
        # Figure out how to print on front-end message "Incorrect PIN!"

    
    # 3. Create token
    token = create_token(
        employee_id=employee.id,
        restaurant_id=employee.restaurant_id,
        auth_type="pos"
    )

    return LoginResponse(access_token=token, token_type="bearer")

# Method for users to login to the portal dashboard
@router.post("/login/portal", response_model=LoginResponse)
async def portal_login(request: PortalLoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.username == request.username))
    employee = result.scalar_one_or_none()

    # 1. Employee not found
    if not employee:
        raise UnauthorizedException()
        # Figure out how to print on front-end message "Employee not found."

    # 2. Employee does not have a set password
    if not employee.password_hash:
        raise UnauthorizedException()
        # Figure out how to print on front-end message like "Has the user configured their password yet?"

    # 3. Given pin is incorrect
    if not verify_secret(request.password, employee.password_hash):
        raise UnauthorizedException()
        # Figure out how to print on front-end message "Incorrect password!"

    
    # 4. Create token
    token = create_token(
        employee_id=employee.id,
        restaurant_id=employee.restaurant_id,
        auth_type="portal",
        name=employee.name
    )

    return LoginResponse(access_token=token, token_type="bearer")