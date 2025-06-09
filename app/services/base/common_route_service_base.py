from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.common_route_repository import CommonRouteRepository
from app.models.models import CommonRoute
from app.services.base.base_service import BaseService


class CommonRouteServiceBase(BaseService):
    """
    CommonRoute に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[CommonRouteRepository] = None):
        self.repository = repository or CommonRouteRepository()

    def get(self, db: Session, id: int) -> Optional[CommonRoute]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[CommonRoute]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: CommonRoute) -> CommonRoute:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: CommonRoute, data: dict) -> CommonRoute:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: CommonRoute) -> None:
        return self.repository.delete(db, instance)