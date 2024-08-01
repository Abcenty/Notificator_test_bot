from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from db.models.base import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    telegram_id: Mapped[int] = mapped_column(Integer)