from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Integer, TIMESTAMP
from datetime import datetime

from db.models.base import Base

class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
    )
    text: Mapped[str] = mapped_column(String(256), nullable=False)
    reminder_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)