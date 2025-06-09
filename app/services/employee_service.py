from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.employee_repository import EmployeeRepository
from app.models.models import Employee
from app.services.base.base_service import BaseService


class EmployeeService(BaseService):
    """
    Employee に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[EmployeeRepository] = None):
        self.dao = dao or EmployeeRepository()

    def get(self, db: Session, id: int) -> Optional[Employee]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Employee):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Employee, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Employee):
        return self.dao.delete(db, instance)