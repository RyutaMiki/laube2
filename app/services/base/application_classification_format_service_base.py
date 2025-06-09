from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.application_classification_format_repository import ApplicationClassificationFormatRepository
from app.models.models import ApplicationClassificationFormat
from app.services.base.base_service import BaseService


class ApplicationClassificationFormatServiceBase(BaseService):
    """
    ApplicationClassificationFormat に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[ApplicationClassificationFormatRepository] = None):
        self.repository = repository or ApplicationClassificationFormatRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationClassificationFormat]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[ApplicationClassificationFormat]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationClassificationFormat) -> ApplicationClassificationFormat:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: ApplicationClassificationFormat, data: dict) -> ApplicationClassificationFormat:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: ApplicationClassificationFormat) -> None:
        return self.repository.delete(db, instance)