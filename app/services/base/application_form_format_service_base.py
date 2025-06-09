from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.application_form_format_repository import ApplicationFormFormatRepository
from app.models.models import ApplicationFormFormat
from app.services.base.base_service import BaseService


class ApplicationFormFormatServiceBase(BaseService):
    """
    ApplicationFormFormat に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[ApplicationFormFormatRepository] = None):
        self.repository = repository or ApplicationFormFormatRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationFormFormat]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[ApplicationFormFormat]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationFormFormat) -> ApplicationFormFormat:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: ApplicationFormFormat, data: dict) -> ApplicationFormFormat:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: ApplicationFormFormat) -> None:
        return self.repository.delete(db, instance)