from app.models.models import IndividualRoute
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.individual_route_dao_base import IndividualRouteDaoBase

class IndividualRouteDao(IndividualRouteDaoBase):
    """
    IndividualRoute に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[IndividualRoute]:
            return db_session.query(IndividualRoute).filter(IndividualRoute.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください