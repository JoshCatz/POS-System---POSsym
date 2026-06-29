from sqlalchemy import select
from app.schemas.rbac import AssignRoleRequest
from app.models.rbac import Role, EmployeeRole
from app.services.employee import get_employee
from app.errors import NotFoundException, RedundantException


ROLE_PRIORITY = {
    "admin": 1,
    "manager": 2,
    "employee": 3
}

async def get_all_roles(db):
    result = await db.execute(select(Role))
    roles = result.scalars().all()

    return roles

async def get_employee_roles(db, employee_id, restaurant_id):
    employee = await get_employee(db, employee_id, restaurant_id)

    result = await db.execute(
        select(Role).join(
            EmployeeRole, 
            EmployeeRole.role_id == Role.id
        ).where(
            EmployeeRole.employee_id == employee_id
        )
    )

    employee_roles = result.scalars().all()

    return employee_roles

async def assign_role(db, data: AssignRoleRequest, employee_id, restaurant_id):
    employee = await get_employee(db, employee_id, restaurant_id)

    # check roles
    result = await db.execute(select(Role).where(Role.id == data.role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise NotFoundException(f"Role {data.role_id} does not exist")

    # check employee/role relation
    result = await db.execute(select(EmployeeRole).where(EmployeeRole.role_id == data.role_id, EmployeeRole.employee_id == employee_id))
    existing_role = result.scalar_one_or_none()
    if existing_role:
        raise RedundantException(f"Employee/Role relationship already exist")

    employee_role = EmployeeRole(employee_id=employee_id, role_id=data.role_id)
    db.add(employee_role)
    await db.commit()
    await db.refresh(employee_role)

    return employee_role
    

async def remove_role(db, role_id, employee_id, restaurant_id):
    employee = await get_employee(db, employee_id, restaurant_id)
    result = await db.execute(select(EmployeeRole).where(EmployeeRole.role_id == role_id, EmployeeRole.employee_id == employee_id))
    role_to_delete = result.scalar_one_or_none()

    if not role_to_delete:
        raise NotFoundException(f"Role assignment not found for {employee_id}")
    
    await db.delete(role_to_delete)
    await db.commit()

async def get_highest_role(db, employee_id, restaurant_id):
    roles = await get_employee_roles(db, employee_id, restaurant_id)
    role_names = [role.name for role in roles]

    if not role_names:
        return "employee"

    highest = min(role_names, key=lambda name: ROLE_PRIORITY.get(name, 0))

    return highest





