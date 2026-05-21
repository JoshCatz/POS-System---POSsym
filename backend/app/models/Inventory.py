from app.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    quantity: Mapped[int] = mapped_column()

    