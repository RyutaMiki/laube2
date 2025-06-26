from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.application_form_repository import ApplicationFormRepository
from app.models.models import ApplicationForm
from app.services.base.base_service import BaseService


class ApplicationFormService(BaseService):
    """
    ApplicationForm に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ApplicationFormRepository] = None):
        self.dao = dao or ApplicationFormRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationForm]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationForm):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ApplicationForm, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ApplicationForm):
        return self.dao.delete(db, instance)