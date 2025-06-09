from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.activity_object_repository import ActivityObjectRepository
from app.models.models import ActivityObject
from app.services.base.base_service import BaseService


class ActivityObjectService(BaseService):
    """
    ActivityObject に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ActivityObjectRepository] = None):
        self.dao = dao or ActivityObjectRepository()

    def get(self, db: Session, id: int) -> Optional[ActivityObject]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ActivityObject):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ActivityObject, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ActivityObject):
        return self.dao.delete(db, instance)