from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.employee_repository import EmployeeRepository
from app.models.models import Employee
from app.services.base.base_service import BaseService


class EmployeeServiceBase(BaseService):
    """
    Employee に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[EmployeeRepository] = None):
        self.repository = repository or EmployeeRepository()

    def get(self, db: Session, id: int) -> Optional[Employee]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[Employee]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: Employee) -> Employee:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: Employee, data: dict) -> Employee:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: Employee) -> None:
        return self.repository.delete(db, instance)