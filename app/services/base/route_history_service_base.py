from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.route_history_repository import RouteHistoryRepository
from app.models.models import RouteHistory
from app.services.base.base_service import BaseService


class RouteHistoryServiceBase(BaseService):
    """
    RouteHistory に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[RouteHistoryRepository] = None):
        self.repository = repository or RouteHistoryRepository()

    def get(self, db: Session, id: int) -> Optional[RouteHistory]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[RouteHistory]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: RouteHistory) -> RouteHistory:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: RouteHistory, data: dict) -> RouteHistory:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: RouteHistory) -> None:
        return self.repository.delete(db, instance)