from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.rework_route_repository import ReworkRouteRepository
from app.models.models import ReworkRoute
from app.services.base.base_service import BaseService


class ReworkRouteService(BaseService):
    """
    ReworkRoute に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ReworkRouteRepository] = None):
        self.dao = dao or ReworkRouteRepository()

    def get(self, db: Session, id: int) -> Optional[ReworkRoute]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ReworkRoute):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ReworkRoute, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ReworkRoute):
        return self.dao.delete(db, instance)