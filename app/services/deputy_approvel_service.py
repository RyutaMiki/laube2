from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.deputy_approvel_repository import DeputyApprovelRepository
from app.models.models import DeputyApprovel
from app.services.base.base_service import BaseService


class DeputyApprovelService(BaseService):
    """
    DeputyApprovel に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[DeputyApprovelRepository] = None):
        self.dao = dao or DeputyApprovelRepository()

    def get(self, db: Session, id: int) -> Optional[DeputyApprovel]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: DeputyApprovel):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: DeputyApprovel, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: DeputyApprovel):
        return self.dao.delete(db, instance)