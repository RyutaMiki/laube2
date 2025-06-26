from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.tenant_repository import TenantRepository
from app.models.models import Tenant
from app.services.base.base_service import BaseService


class TenantService(BaseService):
    """
    Tenant に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[TenantRepository] = None):
        self.dao = dao or TenantRepository()

    def get(self, db: Session, id: int) -> Optional[Tenant]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Tenant):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Tenant, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Tenant):
        return self.dao.delete(db, instance)