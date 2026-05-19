from app.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

class Order(Base):
    pass

class Order_Item(Base):
    pass

class Order_Item_Modifier(Base):
    pass


