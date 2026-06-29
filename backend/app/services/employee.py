from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import UnauthorizedException
from app.models.employee import Employee
from app.services.auth import create_pin_lookup_hash, hash_secret
from app.schemas.employee import EmployeeCreateRequest
from app.errors import NotFoundException
from app.config import settings

# Checks to see if a requested PIN is already in use at a location
async def set_employee_pin(db: AsyncSession, employee: Employee, raw_pin: str,) -> Employee:
    pin_lookup_hash = create_pin_lookup_hash(
        restaurant_id=employee.restaurant_id,
        pin=raw_pin,
    )

    result = await db.execute(
        select(Employee).where(
            Employee.restaurant_id == employee.restaurant_id,
            Employee.pin_lookup_hash == pin_lookup_hash,
            Employee.id != employee.id,
        )
    )

    existing_employee = result.scalar_one_or_none()

    if existing_employee:
        raise ValueError("PIN is already in use for this restaurant.")

    employee.pin_hash = hash_secret(raw_pin)
    employee.pin_lookup_hash = pin_lookup_hash

    return employee

# Checks at account creation if a password meets the strength requirements
def validate_password_strength(raw_password: str, username: str | None = None) -> None:
    if len(raw_password) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    if raw_password.strip() != raw_password:
        raise ValueError("Password cannot start or end with whitespace.")

    if username and username.lower() in raw_password.lower():
        raise ValueError("Password cannot contain the username.")

    has_letter = any(char.isalpha() for char in raw_password)
    has_number = any(char.isdigit() for char in raw_password)

    if not has_letter or not has_number:
        raise ValueError("Password must contain at least one letter and one number.")

# Sets an employee's password to the validated requested password
def set_employee_password(employee: Employee, raw_password: str) -> Employee:
    validate_password_strength(raw_password, employee.username)

    employee.password_hash = hash_secret(raw_password)

    return employee

# Parent function to create an employee object and store it in the Postgres database
async def create_employee(db: AsyncSession, data: EmployeeCreateRequest) -> Employee:
    employee = Employee(
        restaurant_id=data.restaurant_id,
        name=data.name,
        username=data.username,
        is_active=True,
    )

    if data.pin:
        await set_employee_pin(db, employee, data.pin)

    if data.password:
        set_employee_password(employee, data.password)

    db.add(employee)
    await db.commit()
    await db.refresh(employee)

    return employee

# Function to retrieve employee object from database
async def get_employee(db: AsyncSession, employee_id: int, restaurant_id: int):
    result = await db.execute(select(Employee).where(Employee.id == employee_id, Employee.restaurant_id == restaurant_id))
    item = result.scalar_one_or_none()

    if not item:
        raise NotFoundException(f"Employee not found: {employee_id}")

    return item

async def get_all_employees(db: AsyncSession, restaurant_id):
    result = await db.execute(select(Employee).where(Employee.restaurant_id == restaurant_id))
    employees = result.scalars().all()

    return employees