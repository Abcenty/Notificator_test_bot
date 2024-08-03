from datetime import datetime, timedelta
from sqlalchemy import select
from db.database import session_factory
from db.models.notes import Notes
from logger import logger


class NotesGateway:
    @staticmethod
    def list(user_id: int):
        with session_factory() as session:
            query = select(Notes).where(Notes.user_id == user_id)
            result = session.execute(query)
            scalars = result.scalars().all()
            return [note for note in scalars]

    @staticmethod
    def get_for_remind(user_id: int, text: str):
        with session_factory() as session:
            now = datetime.now()
            logger.info(f"now: {now}")
            query = session.query(Notes.text).filter(
                now + timedelta(minutes=10) >= Notes.reminder_time,
                Notes.user_id == user_id,
                Notes.text == text,
            )
            result = session.execute(query)
            note = result.scalars().first()
            return note

    @staticmethod
    def create(user_id: int, text: str, reminder_time: datetime):
        with session_factory() as session:
            session.add(Notes(user_id=user_id, text=text, reminder_time=reminder_time))
            session.commit()
