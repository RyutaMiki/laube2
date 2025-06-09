from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.application_form_route_repository import ApplicationFormRouteRepository
from app.models.models import ApplicationFormRoute
from app.services.base.base_service import BaseService


class ApplicationFormRouteServiceBase(BaseService):
    """
    ApplicationFormRoute に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[ApplicationFormRouteRepository] = None):
        self.repository = repository or ApplicationFormRouteRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationFormRoute]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[ApplicationFormRoute]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationFormRoute) -> ApplicationFormRoute:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: ApplicationFormRoute, data: dict) -> ApplicationFormRoute:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: ApplicationFormRoute) -> None:
        return self.repository.delete(db, instance)