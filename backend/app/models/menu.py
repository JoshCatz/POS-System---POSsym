from app.models.base import Base, TimestampMixin
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal

# Categories keep menu items organized. i.e. Burgers, Sandwiches, Sides, Drinks, etc.
class MenuCatgeory(Base):
  __tablename__ = "menu_categories"

  id: Mapped[int] = mapped_column(primary_key=True)
  restaurant_id = mapped_column(ForeignKey("restaurants.id"), nullable=False)

  name: Mapped[str] = mapped_column(String(100), nullable=False)
  display_order: Mapped[int] = mapped_column(nullable=False, default=0)
  is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

# Specific items to be purchased
class MenuItem(Base, TimestampMixin):
  __tablename__ = "manu_items"

  id: Mapped[int] = mapped_column(primary_key=True)
  restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
  cateogry_id: Mapped[int | None] = mapped_column(ForeignKey("menu_categories.id"), nullable=False)

  name: Mapped[str] = mapped_column(String(255), nullable=False)
  description: Mapped[str | None] = mapped_column(String(500), nullable=True)

  price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

  is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
