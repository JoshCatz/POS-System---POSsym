from app.models.base import Base, TimestampMixin
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from decimal import Decimal

# Table to store records for all processed payments
class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    provider_payment_id: Mapped[str]= mapped_column(String(255), nullable=False)
    
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    tip_amount: Mapped[Decimal] = mapped_column(Numeric(10,2), default=Decimal("0.00"), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(10,2), default=Decimal("0.00"), nullable=False)
    
    method: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(100))

    paid_at: Mapped[datetime | None] = mapped_column(nullable=True)

# Table to store records for all processed refunds
class Refund(Base):
    __tablename__ = "refunds"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payments.id"), nullable=False)
    
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[str] = mapped_column(String(100), nullable=False, default="pending")
    refunded_at: Mapped[datetime | None] = mapped_column(nullable=True)
