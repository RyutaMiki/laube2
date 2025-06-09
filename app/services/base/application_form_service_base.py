from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.application_form_repository import ApplicationFormRepository
from app.models.models import ApplicationForm
from app.services.base.base_service import BaseService


class ApplicationFormServiceBase(BaseService):
    """
    ApplicationForm に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[ApplicationFormRepository] = None):
        self.repository = repository or ApplicationFormRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationForm]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[ApplicationForm]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationForm) -> ApplicationForm:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: ApplicationForm, data: dict) -> ApplicationForm:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: ApplicationForm) -> None:
        return self.repository.delete(db, instance)