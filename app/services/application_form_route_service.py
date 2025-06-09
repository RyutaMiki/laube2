from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.application_form_route_repository import ApplicationFormRouteRepository
from app.models.models import ApplicationFormRoute
from app.services.base.base_service import BaseService


class ApplicationFormRouteService(BaseService):
    """
    ApplicationFormRoute に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ApplicationFormRouteRepository] = None):
        self.dao = dao or ApplicationFormRouteRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationFormRoute]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationFormRoute):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ApplicationFormRoute, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ApplicationFormRoute):
        return self.dao.delete(db, instance)