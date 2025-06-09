from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.common_activity_repository import CommonActivityRepository
from app.models.models import CommonActivity
from app.services.base.base_service import BaseService


class CommonActivityServiceBase(BaseService):
    """
    CommonActivity に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[CommonActivityRepository] = None):
        self.repository = repository or CommonActivityRepository()

    def get(self, db: Session, id: int) -> Optional[CommonActivity]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[CommonActivity]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: CommonActivity) -> CommonActivity:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: CommonActivity, data: dict) -> CommonActivity:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: CommonActivity) -> None:
        return self.repository.delete(db, instance)