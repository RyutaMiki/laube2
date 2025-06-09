from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.tenants_repository import TenantsRepository
from app.models.models import Tenants
from app.services.base.base_service import BaseService


class TenantsService(BaseService):
    """
    Tenants に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[TenantsRepository] = None):
        self.dao = dao or TenantsRepository()

    def get(self, db: Session, id: int) -> Optional[Tenants]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Tenants):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Tenants, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Tenants):
        return self.dao.delete(db, instance)