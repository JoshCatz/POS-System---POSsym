from app.models.base import Base, TimestampMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

# Each individual employee within a restaurant
class Employee(Base, TimestampMixin):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    
    name: Mapped[str] = mapped_column(String(255))
    pin_hash: Mapped[str] = mapped_column(String(255))  
    password_hash: Mapped[str] = mapped_column(String(255))
    
    is_active: Mapped[bool] = mapped_column(default=True)

# Employe's job within the restaurant. i.e. Server, Bartender, Manager, Cook, etc.
class Position(Base, TimestampMixin):
    __tablename__ = "positions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))

# Connects employees to their position
class Employee_Position(Base, TimestampMixin):
    __tablename__ = "employee_positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    
    __table_args__ = (
        UniqueConstraint("employee_id", "position_id")
    )

# Shift worked by an employee
class Shift(Base, TimestampMixin):
    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    employee_position_id: Mapped[int] = mapped_column(ForeignKey("employee_positions.id"))
    clocked_in_at: Mapped[datetime] = mapped_column()
    clocked_out_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
