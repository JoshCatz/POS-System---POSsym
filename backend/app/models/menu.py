from app.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

class Menu(Base):
    pass

class Category(Base):
    pass

class Modifier_Group(Base):
    pass

class Modifier(Base):
    pass