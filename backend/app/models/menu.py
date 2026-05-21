from app.models.base import Base
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)


class Modifier_Group(Base):
    __tablename__ = "modifier_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    menu_id: Mapped[int] = mapped_column(ForeignKey("menus.id"))
    name: Mapped[str] = mapped_column(String(100))

class Modifier(Base):
    __tablename__ = "modifiers"

    id: Mapped[int] = mapped_column(primary_key=True)
    modifier_group_id: Mapped[int] = mapped_column(ForeignKey("modifier_groups.id"))
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), default=0.00)

