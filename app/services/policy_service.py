from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.policy_repository import PolicyRepository
from app.models.models import Policy
from app.services.base.base_service import BaseService


class PolicyService(BaseService):
    """
    Policy に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[PolicyRepository] = None):
        self.dao = dao or PolicyRepository()

    def get(self, db: Session, id: int) -> Optional[Policy]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Policy):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Policy, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Policy):
        return self.dao.delete(db, instance)