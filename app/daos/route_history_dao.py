from app.models.models import RouteHistory
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.route_history_dao_base import RouteHistoryDaoBase

class RouteHistoryDao(RouteHistoryDaoBase):
    """
    RouteHistory に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[RouteHistory]:
            return db_session.query(RouteHistory).filter(RouteHistory.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください