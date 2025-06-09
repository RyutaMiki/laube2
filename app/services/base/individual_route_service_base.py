from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.individual_route_repository import IndividualRouteRepository
from app.models.models import IndividualRoute
from app.services.base.base_service import BaseService


class IndividualRouteServiceBase(BaseService):
    """
    IndividualRoute に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[IndividualRouteRepository] = None):
        self.repository = repository or IndividualRouteRepository()

    def get(self, db: Session, id: int) -> Optional[IndividualRoute]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[IndividualRoute]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: IndividualRoute) -> IndividualRoute:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: IndividualRoute, data: dict) -> IndividualRoute:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: IndividualRoute) -> None:
        return self.repository.delete(db, instance)