from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.tenant_user_repository import TenantUserRepository
from app.models.models import TenantUser
from app.services.base.base_service import BaseService


class TenantUserService(BaseService):
    """
    TenantUser に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[TenantUserRepository] = None):
        self.dao = dao or TenantUserRepository()

    def get(self, db: Session, id: int) -> Optional[TenantUser]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: TenantUser):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: TenantUser, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: TenantUser):
        return self.dao.delete(db, instance)