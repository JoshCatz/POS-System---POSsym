from app.models.base import Base, TimestampMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

# Roles to control access. i.e. employee, manager, admin
class Role(Base, TimestampMixin):
  __tablename__ = "roles"

id: Mapped[int] = mapped_column(primary_key=True)
name: Mapped[str] = mapped_column(String(50), nullable=False)
description: Mapped[str | None] = mapped_column(String(255), nullable=True)

__table_args__ = (
  UniqueConstraint("name", name="uq_roles_name"),
)

# Specific capabilities of each role
class Permission(Base):
  __tablename = "permissions"

  id = Mapped[int] = mapped_column(primary_key=True)
  code: Mapped[str] = mapped_column(String(100), nullable=False)
  description: Mapped[str | None] = mapped_column(String(255), nullable=True)

  __table_args__ = (
    UniqueConstraint("code", name="uq_permissions_code"),
  )

# Connect roles to their permissions
class RolePermission(Base):
  __tablename__ = "role_permissions"

  id: Mapped[int] = mapped_column(primary_key=True)
  role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
  permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"), nullable=False)

  __table_args__ = (
    UniqueConstraint("role_id", "permission_id", name="uq_role_permissions_role_permission"),
  )

# Connect employees to their roles
class EmployeeRole(Base):
  __tablename__ = "employee_roles"

  id: Mapped[int] = mapped_column(primary_key=True)
  employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
  role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

  __table_args__ = (
    UniqueConstraint("employee_id", "role_id", name="uq_employee_roles_employee_role"),
  )
