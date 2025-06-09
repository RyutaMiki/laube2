from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.approval_policy_repository import ApprovalPolicyRepository
from app.models.models import ApprovalPolicy
from app.services.base.base_service import BaseService


class ApprovalPolicyService(BaseService):
    """
    ApprovalPolicy に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ApprovalPolicyRepository] = None):
        self.dao = dao or ApprovalPolicyRepository()

    def get(self, db: Session, id: int) -> Optional[ApprovalPolicy]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ApprovalPolicy):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ApprovalPolicy, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ApprovalPolicy):
        return self.dao.delete(db, instance)