from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.individual_route_repository import IndividualRouteRepository
from app.models.models import IndividualRoute
from app.services.base.base_service import BaseService


class IndividualRouteService(BaseService):
    """
    IndividualRoute に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[IndividualRouteRepository] = None):
        self.dao = dao or IndividualRouteRepository()

    def get(self, db: Session, id: int) -> Optional[IndividualRoute]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: IndividualRoute):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: IndividualRoute, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: IndividualRoute):
        return self.dao.delete(db, instance)