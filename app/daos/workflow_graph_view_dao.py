from app.models.models import WorkflowGraphView
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.workflow_graph_view_dao_base import WorkflowGraphViewDaoBase

class WorkflowGraphViewDao(WorkflowGraphViewDaoBase):
    """
    WorkflowGraphView に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[WorkflowGraphView]:
            return db_session.query(WorkflowGraphView).filter(WorkflowGraphView.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください