from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.user_role_repository import UserRoleRepository
from app.models.models import UserRole
from app.services.base.base_service import BaseService


class UserRoleService(BaseService):
    """
    UserRole に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[UserRoleRepository] = None):
        self.dao = dao or UserRoleRepository()

    def get(self, db: Session, id: int) -> Optional[UserRole]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: UserRole):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: UserRole, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: UserRole):
        return self.dao.delete(db, instance)