from app.models.models import ActivityTransit
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.activity_transit_dao_base import ActivityTransitDaoBase

class ActivityTransitDao(ActivityTransitDaoBase):
    """
    ActivityTransit に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ActivityTransit]:
            return db_session.query(ActivityTransit).filter(ActivityTransit.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください