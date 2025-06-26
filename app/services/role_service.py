from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.role_repository import RoleRepository
from app.models.models import Role
from app.services.base.base_service import BaseService


class RoleService(BaseService):
    """
    Role に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[RoleRepository] = None):
        self.dao = dao or RoleRepository()

    def get(self, db: Session, id: int) -> Optional[Role]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Role):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Role, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Role):
        return self.dao.delete(db, instance)