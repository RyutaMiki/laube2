from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.appended_repository import AppendedRepository
from app.models.models import Appended
from app.services.base.base_service import BaseService


class AppendedService(BaseService):
    """
    Appended に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[AppendedRepository] = None):
        self.dao = dao or AppendedRepository()

    def get(self, db: Session, id: int) -> Optional[Appended]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Appended):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Appended, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Appended):
        return self.dao.delete(db, instance)