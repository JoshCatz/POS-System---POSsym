from app.models.base import Base
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))       
    paid: Mapped[bool] = mapped_column(default=False)
