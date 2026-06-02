from app.models.base import Base, TimestampMixin
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from decimal import Decimal

# Whole order as it exist in sales reporting
class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    table_id: Mapped[int | None] = mapped_column(ForeignKey("tables.id"), nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")
    order_type: Mapped[str] = mapped_column(String(50), nullable=False, default="dine_in")

    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    tax_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    discount_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    opened_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    closed_at: Mapped[datetime | None] = mapped_column(nullable=True)

# Individual tables within each restaurant
class Table(Base, TimestampMixin):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    employee_id: Mapped[int | None] = mapped_column(ForiegnKey("employees.id"), nullable=True)
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_seated: Mapped[bool] = mapped_column(nullable=False, default=False)

# Individual items within an order
class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"), nullable=False)

    quantity: Mapped[int] = mapped_column(nullable=False, default=1)

    item_name_snapshot: Mapped[str] = mapped_column(String(255), nullable=False)
    unit_price_snapshot: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
