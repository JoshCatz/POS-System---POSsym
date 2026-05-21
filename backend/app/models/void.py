from app.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

class Void(Base):
    __tablename__ = "voids"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_item_id: Mapped[int] = mapped_column(ForeignKey("order_items.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    reason: Mapped[str] = mapped_column(String(255))

    