from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.field_visibility_repository import FieldVisibilityRepository
from app.models.models import FieldVisibility
from app.services.base.base_service import BaseService


class FieldVisibilityService(BaseService):
    """
    FieldVisibility に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[FieldVisibilityRepository] = None):
        self.dao = dao or FieldVisibilityRepository()

    def get(self, db: Session, id: int) -> Optional[FieldVisibility]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: FieldVisibility):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: FieldVisibility, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: FieldVisibility):
        return self.dao.delete(db, instance)