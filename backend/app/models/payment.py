from app.models.base import Base
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    provider: Mapped[str] = mapped_column(String(100))
    provider_payment_id: Mapped[str]= mapped_column(String(255))
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2))
    tip_amount: Mapped[Decimal] = mapped_column(Numeric(10,2), default=0.00)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(10,2))
    method: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(100))

class Refund(Base):
    __tablename__ = "refunds"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payments.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2))
    reason: Mapped[str] = mapped_column(String(255))