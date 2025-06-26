from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.role_permission_repository import RolePermissionRepository
from app.models.models import RolePermission
from app.services.base.base_service import BaseService


class RolePermissionService(BaseService):
    """
    RolePermission に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[RolePermissionRepository] = None):
        self.dao = dao or RolePermissionRepository()

    def get(self, db: Session, id: int) -> Optional[RolePermission]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: RolePermission):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: RolePermission, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: RolePermission):
        return self.dao.delete(db, instance)