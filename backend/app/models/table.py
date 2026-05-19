from app.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

class Tables(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id")) 
    table_number: Mapped[int]
    status: Mapped[str] = mapped_column(String(100)) # open, occupied, reserved, closed
    employee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    order_id: Mapped[Optional[int]] = mapped_column(ForeignKey("orders.id"), nullable=True)

class Table_Party(Base):
    __tablename__ = "table_party"

    id: Mapped[int] = mapped_column(primary_key=True)
    primary_table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    joined_table_id: Mapped[int] = mapped_column(ForeignKey("tables.id")) 