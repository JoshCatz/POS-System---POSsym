from app.models.base import Base
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Tip(Base):
    __tablename__ = "tips"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payments.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2))
    