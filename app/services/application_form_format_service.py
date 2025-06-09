from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.application_form_format_repository import ApplicationFormFormatRepository
from app.models.models import ApplicationFormFormat
from app.services.base.base_service import BaseService


class ApplicationFormFormatService(BaseService):
    """
    ApplicationFormFormat に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ApplicationFormFormatRepository] = None):
        self.dao = dao or ApplicationFormFormatRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationFormFormat]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationFormFormat):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ApplicationFormFormat, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ApplicationFormFormat):
        return self.dao.delete(db, instance)