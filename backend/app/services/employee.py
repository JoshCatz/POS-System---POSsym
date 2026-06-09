from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import UnauthorizedException
from app.models.employee import Employee
from app.services.auth import create_pin_lookup_hash, hash_secret
from app.schemas.employee import EmployeeCreateRequest


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


def set_employee_password(employee: Employee, raw_password: str) -> Employee:
    validate_password_strength(raw_password, employee.username)

    employee.password_hash = hash_secret(raw_password)

    return employee

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