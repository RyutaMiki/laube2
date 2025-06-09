from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.activity_transit_repository import ActivityTransitRepository
from app.models.models import ActivityTransit
from app.services.base.base_service import BaseService


class ActivityTransitServiceBase(BaseService):
    """
    ActivityTransit に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[ActivityTransitRepository] = None):
        self.repository = repository or ActivityTransitRepository()

    def get(self, db: Session, id: int) -> Optional[ActivityTransit]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[ActivityTransit]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: ActivityTransit) -> ActivityTransit:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: ActivityTransit, data: dict) -> ActivityTransit:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: ActivityTransit) -> None:
        return self.repository.delete(db, instance)