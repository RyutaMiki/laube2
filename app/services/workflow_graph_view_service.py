from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.workflow_graph_view_repository import WorkflowGraphViewRepository
from app.models.models import WorkflowGraphView
from app.services.base.base_service import BaseService


class WorkflowGraphViewService(BaseService):
    """
    WorkflowGraphView に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[WorkflowGraphViewRepository] = None):
        self.dao = dao or WorkflowGraphViewRepository()

    def get(self, db: Session, id: int) -> Optional[WorkflowGraphView]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: WorkflowGraphView):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: WorkflowGraphView, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: WorkflowGraphView):
        return self.dao.delete(db, instance)