from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.employee_group_repository import EmployeeGroupRepository
from app.models.models import EmployeeGroup
from app.services.base.base_service import BaseService


class EmployeeGroupService(BaseService):
    """
    EmployeeGroup に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[EmployeeGroupRepository] = None):
        self.dao = dao or EmployeeGroupRepository()

    def get(self, db: Session, id: int) -> Optional[EmployeeGroup]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: EmployeeGroup):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: EmployeeGroup, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: EmployeeGroup):
        return self.dao.delete(db, instance)