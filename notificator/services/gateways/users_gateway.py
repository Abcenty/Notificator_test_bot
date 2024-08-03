from sqlalchemy import select
from db.database import session_factory
from db.models.users import Users


class UserGateway:
    @staticmethod
    def get(telegram_id: int):
        with session_factory() as session:
            query = select(Users).where(Users.telegram_id == telegram_id)
            result = session.execute(query)
            user = result.scalar()
            return user

    def create(self, name: str, email: str, telegram_id: int):
        with session_factory() as session:
            session.add(Users(name=name, email=email, telegram_id=telegram_id))
            session.commit()
