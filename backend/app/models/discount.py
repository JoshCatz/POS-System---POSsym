from app.models.base import Base
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Discount(Base):
    __tablename__ = "discounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    percent: Mapped[Decimal] = mapped_column(Numeric(10,2))

class Tax_Rate(Base):
    __tablename__ = "tax_rates"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    name: Mapped[str] = mapped_column(String(100))
    percent: Mapped[Decimal] = mapped_column(Numeric(10,2))
    