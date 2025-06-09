from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.group_repository import GroupRepository
from app.models.models import Group
from app.services.base.base_service import BaseService


class GroupService(BaseService):
    """
    Group に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[GroupRepository] = None):
        self.dao = dao or GroupRepository()

    def get(self, db: Session, id: int) -> Optional[Group]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Group):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Group, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Group):
        return self.dao.delete(db, instance)