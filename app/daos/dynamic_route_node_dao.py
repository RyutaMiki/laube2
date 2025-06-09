from app.models.models import DynamicRouteNode
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.dynamic_route_node_dao_base import DynamicRouteNodeDaoBase

class DynamicRouteNodeDao(DynamicRouteNodeDaoBase):
    """
    DynamicRouteNode に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[DynamicRouteNode]:
            return db_session.query(DynamicRouteNode).filter(DynamicRouteNode.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください