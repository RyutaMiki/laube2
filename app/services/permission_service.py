from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.permission_repository import PermissionRepository
from app.models.models import Permission
from app.services.base.base_service import BaseService


class PermissionService(BaseService):
    """
    Permission に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[PermissionRepository] = None):
        self.dao = dao or PermissionRepository()

    def get(self, db: Session, id: int) -> Optional[Permission]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Permission):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Permission, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Permission):
        return self.dao.delete(db, instance)