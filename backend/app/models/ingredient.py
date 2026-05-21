from app.models.base import Base
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10,2))

class Menu_Ingredient(Base):
    __tablename__ = "menu_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    menu_id: Mapped[int] = mapped_column(ForeignKey("menus.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))

