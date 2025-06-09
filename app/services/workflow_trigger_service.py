from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.workflow_trigger_repository import WorkflowTriggerRepository
from app.models.models import WorkflowTrigger
from app.services.base.base_service import BaseService


class WorkflowTriggerService(BaseService):
    """
    WorkflowTrigger に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[WorkflowTriggerRepository] = None):
        self.dao = dao or WorkflowTriggerRepository()

    def get(self, db: Session, id: int) -> Optional[WorkflowTrigger]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: WorkflowTrigger):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: WorkflowTrigger, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: WorkflowTrigger):
        return self.dao.delete(db, instance)