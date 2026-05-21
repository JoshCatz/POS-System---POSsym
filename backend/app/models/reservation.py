from app.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    table_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tables.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    number_of_guests: Mapped[int] = mapped_column()
    date_time: Mapped[datetime] = mapped_column()
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50))
