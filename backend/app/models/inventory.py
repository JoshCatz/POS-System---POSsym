from app.models.base import Base, TimestampMixin
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

# Ingredient item as it exist in stock. i.e. Ground beef, Lettuce, Ketchup, etc.
class InventoryItem(Base, TimestampMixin):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)

    quantity_on_hand: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    reorder_threshold: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)

    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

# Bridge to connect ingredients to menu items for stock updates. i.e. 0.25lb Ground beef -> 1 Hamburger
class RecipeIngredient(Base, TimestampMixin):
    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)

    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"), nullable=False)
    inventory_item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"), nullable=False)

    quantity_required: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

# Log inventory adjustments
class StockAdjustment(Base, TimestampMixin):
    __tablename__ = "stock_adjustments"

    id: Mapped[int] = mapped_column(primary_key=True)

    inventory_item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)

    quantity_change: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    adjustment_type: Mapped[str] = mapped_column(String(255), nullable=False)
    adjusted_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
