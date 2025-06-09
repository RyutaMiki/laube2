from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.appended_repository import AppendedRepository
from app.models.models import Appended
from app.services.base.base_service import BaseService


class AppendedServiceBase(BaseService):
    """
    Appended に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[AppendedRepository] = None):
        self.repository = repository or AppendedRepository()

    def get(self, db: Session, id: int) -> Optional[Appended]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[Appended]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: Appended) -> Appended:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: Appended, data: dict) -> Appended:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: Appended) -> None:
        return self.repository.delete(db, instance)