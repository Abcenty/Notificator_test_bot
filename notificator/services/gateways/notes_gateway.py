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
    def get(name: str):
        with session_factory() as session:
            query = select(Notes).where(Notes.name == name) 
            result = session.execute(query)
            notes = result.scalar()
            return notes
        
    @staticmethod  
    def create(user_id: int, text: str, reminder_time: datetime):
        with session_factory() as session:
            session.add(Notes(user_id=user_id, text=text, reminder_time=reminder_time))
            session.commit()
            
    @staticmethod
    def delete(name: str):
        with session_factory() as session:
            query = session.query(Notes).filter(Notes.name == name).first()
            session.delete(query)
            session.commit()