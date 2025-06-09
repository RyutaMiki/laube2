from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.application_object_repository import ApplicationObjectRepository
from app.models.models import ApplicationObject
from app.services.base.base_service import BaseService


class ApplicationObjectServiceBase(BaseService):
    """
    ApplicationObject に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[ApplicationObjectRepository] = None):
        self.repository = repository or ApplicationObjectRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationObject]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[ApplicationObject]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationObject) -> ApplicationObject:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: ApplicationObject, data: dict) -> ApplicationObject:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: ApplicationObject) -> None:
        return self.repository.delete(db, instance)