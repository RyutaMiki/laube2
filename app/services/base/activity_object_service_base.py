from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.activity_object_repository import ActivityObjectRepository
from app.models.models import ActivityObject
from app.services.base.base_service import BaseService


class ActivityObjectServiceBase(BaseService):
    """
    ActivityObject に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[ActivityObjectRepository] = None):
        self.repository = repository or ActivityObjectRepository()

    def get(self, db: Session, id: int) -> Optional[ActivityObject]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[ActivityObject]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: ActivityObject) -> ActivityObject:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: ActivityObject, data: dict) -> ActivityObject:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: ActivityObject) -> None:
        return self.repository.delete(db, instance)