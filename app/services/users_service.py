from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.users_repository import UsersRepository
from app.models.models import Users
from app.services.base.base_service import BaseService


class UsersService(BaseService):
    """
    Users に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[UsersRepository] = None):
        self.dao = dao or UsersRepository()

    def get(self, db: Session, id: int) -> Optional[Users]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Users):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Users, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Users):
        return self.dao.delete(db, instance)