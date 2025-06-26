from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.user_group_repository import UserGroupRepository
from app.models.models import UserGroup
from app.services.base.base_service import BaseService


class UserGroupService(BaseService):
    """
    UserGroup に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[UserGroupRepository] = None):
        self.dao = dao or UserGroupRepository()

    def get(self, db: Session, id: int) -> Optional[UserGroup]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: UserGroup):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: UserGroup, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: UserGroup):
        return self.dao.delete(db, instance)