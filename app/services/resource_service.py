from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.resource_repository import ResourceRepository
from app.models.models import Resource
from app.services.base.base_service import BaseService


class ResourceService(BaseService):
    """
    Resource に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ResourceRepository] = None):
        self.dao = dao or ResourceRepository()

    def get(self, db: Session, id: int) -> Optional[Resource]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Resource):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Resource, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Resource):
        return self.dao.delete(db, instance)