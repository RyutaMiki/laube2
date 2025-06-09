from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.group_repository import GroupRepository
from app.models.models import Group
from app.services.base.base_service import BaseService


class GroupServiceBase(BaseService):
    """
    Group に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[GroupRepository] = None):
        self.repository = repository or GroupRepository()

    def get(self, db: Session, id: int) -> Optional[Group]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[Group]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: Group) -> Group:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: Group, data: dict) -> Group:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: Group) -> None:
        return self.repository.delete(db, instance)