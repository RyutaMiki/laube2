from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.common_activity_repository import CommonActivityRepository
from app.models.models import CommonActivity
from app.services.base.base_service import BaseService


class CommonActivityService(BaseService):
    """
    CommonActivity に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[CommonActivityRepository] = None):
        self.dao = dao or CommonActivityRepository()

    def get(self, db: Session, id: int) -> Optional[CommonActivity]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: CommonActivity):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: CommonActivity, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: CommonActivity):
        return self.dao.delete(db, instance)