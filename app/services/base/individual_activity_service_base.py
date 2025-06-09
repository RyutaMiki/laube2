from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.individual_activity_repository import IndividualActivityRepository
from app.models.models import IndividualActivity
from app.services.base.base_service import BaseService


class IndividualActivityServiceBase(BaseService):
    """
    IndividualActivity に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[IndividualActivityRepository] = None):
        self.repository = repository or IndividualActivityRepository()

    def get(self, db: Session, id: int) -> Optional[IndividualActivity]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[IndividualActivity]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: IndividualActivity) -> IndividualActivity:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: IndividualActivity, data: dict) -> IndividualActivity:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: IndividualActivity) -> None:
        return self.repository.delete(db, instance)