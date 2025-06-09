from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.deputy_approvel_repository import DeputyApprovelRepository
from app.models.models import DeputyApprovel
from app.services.base.base_service import BaseService


class DeputyApprovelServiceBase(BaseService):
    """
    DeputyApprovel に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[DeputyApprovelRepository] = None):
        self.repository = repository or DeputyApprovelRepository()

    def get(self, db: Session, id: int) -> Optional[DeputyApprovel]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[DeputyApprovel]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: DeputyApprovel) -> DeputyApprovel:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: DeputyApprovel, data: dict) -> DeputyApprovel:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: DeputyApprovel) -> None:
        return self.repository.delete(db, instance)