from datetime import datetime
from sqlalchemy import select
from db.database import session_factory
from db.models.notes import Notes


class NotesGateway:
    @staticmethod
    def list(user_id: int):
        with session_factory() as session:
            query = select(Notes).where(Notes.user_id == user_id) 
            result = session.execute(query)
            scalars = result.scalars().all()
            return [note for note in scalars]
         
    @staticmethod
    def get_for_remind(user_id: int):
        with session_factory() as session:
            now = datetime.now()
            query = session.query(Notes.text).filter(Notes.reminder_time <= now, Notes.user_id == user_id)
            result = session.execute(query)
            note = result.scalars().first()
            return note
        
    @staticmethod  
    def create(user_id: int, text: str, reminder_time: datetime):
        with session_factory() as session:
            session.add(Notes(user_id=user_id, text=text, reminder_time=reminder_time))
            session.commit()
            