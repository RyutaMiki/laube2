from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.tenants_repository import TenantsRepository
from app.models.models import Tenants
from app.services.base.base_service import BaseService


class TenantsServiceBase(BaseService):
    """
    Tenants に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[TenantsRepository] = None):
        self.repository = repository or TenantsRepository()

    def get(self, db: Session, id: int) -> Optional[Tenants]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[Tenants]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: Tenants) -> Tenants:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: Tenants, data: dict) -> Tenants:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: Tenants) -> None:
        return self.repository.delete(db, instance)