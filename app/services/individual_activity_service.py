from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.individual_activity_repository import IndividualActivityRepository
from app.models.models import IndividualActivity
from app.services.base.base_service import BaseService


class IndividualActivityService(BaseService):
    """
    IndividualActivity に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[IndividualActivityRepository] = None):
        self.dao = dao or IndividualActivityRepository()

    def get(self, db: Session, id: int) -> Optional[IndividualActivity]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: IndividualActivity):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: IndividualActivity, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: IndividualActivity):
        return self.dao.delete(db, instance)