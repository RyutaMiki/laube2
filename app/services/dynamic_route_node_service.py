from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.dynamic_route_node_repository import DynamicRouteNodeRepository
from app.models.models import DynamicRouteNode
from app.services.base.base_service import BaseService


class DynamicRouteNodeService(BaseService):
    """
    DynamicRouteNode に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[DynamicRouteNodeRepository] = None):
        self.dao = dao or DynamicRouteNodeRepository()

    def get(self, db: Session, id: int) -> Optional[DynamicRouteNode]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: DynamicRouteNode):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: DynamicRouteNode, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: DynamicRouteNode):
        return self.dao.delete(db, instance)