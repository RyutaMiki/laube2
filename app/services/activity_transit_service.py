from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.activity_transit_repository import ActivityTransitRepository
from app.models.models import ActivityTransit
from app.services.base.base_service import BaseService


class ActivityTransitService(BaseService):
    """
    ActivityTransit に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ActivityTransitRepository] = None):
        self.dao = dao or ActivityTransitRepository()

    def get(self, db: Session, id: int) -> Optional[ActivityTransit]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ActivityTransit):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ActivityTransit, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ActivityTransit):
        return self.dao.delete(db, instance)