from app.models.models import CommonRoute
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.common_route_dao_base import CommonRouteDaoBase

class CommonRouteDao(CommonRouteDaoBase):
    """
    CommonRoute に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[CommonRoute]:
            return db_session.query(CommonRoute).filter(CommonRoute.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください