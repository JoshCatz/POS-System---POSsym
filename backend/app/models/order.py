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
    number_of_guests: Mapped[int] = mapped_column()
    paid: Mapped[bool] = mapped_column(default=False)

class Order_Item(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    menu_id: Mapped[int] = mapped_column(ForeignKey("menus.id"))
    seat_num: Mapped[Optional[int]] = mapped_column(nullable=True)
    quantity: Mapped[int] = mapped_column(default=1)
    instructions: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    discount_id: Mapped[Optional[int]] = mapped_column(ForeignKey("discounts.id"), nullable=True)
    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10,2), nullable=True)
    voided: Mapped[bool] = mapped_column(default=False)
    voided_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    void_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

class Order_Item_Modifier(Base):
    __tablename__ = "order_item_modifiers"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_item_id: Mapped[int] = mapped_column(ForeignKey("order_items.id"))
    modifier_id: Mapped[int] = mapped_column(ForeignKey("modifiers.id"))
    price: Mapped[Decimal] = mapped_column(Numeric(10,2))



