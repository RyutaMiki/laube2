from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.common_route_repository import CommonRouteRepository
from app.models.models import CommonRoute
from app.services.base.base_service import BaseService


class CommonRouteService(BaseService):
    """
    CommonRoute に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[CommonRouteRepository] = None):
        self.dao = dao or CommonRouteRepository()

    def get(self, db: Session, id: int) -> Optional[CommonRoute]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: CommonRoute):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: CommonRoute, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: CommonRoute):
        return self.dao.delete(db, instance)