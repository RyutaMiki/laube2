from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.models import User
from app.services.base.base_service import BaseService


class UserService(BaseService):
    """
    User に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[UserRepository] = None):
        self.dao = dao or UserRepository()

    def get(self, db: Session, id: int) -> Optional[User]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: User):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: User, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: User):
        return self.dao.delete(db, instance)