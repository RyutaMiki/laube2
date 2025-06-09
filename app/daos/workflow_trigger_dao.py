from app.models.models import WorkflowTrigger
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.workflow_trigger_dao_base import WorkflowTriggerDaoBase

class WorkflowTriggerDao(WorkflowTriggerDaoBase):
    """
    WorkflowTrigger に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[WorkflowTrigger]:
            return db_session.query(WorkflowTrigger).filter(WorkflowTrigger.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください