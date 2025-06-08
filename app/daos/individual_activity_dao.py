from app.models.models import IndividualActivity
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.individual_activity_dao_base import IndividualActivityDaoBase

class IndividualActivityDao(IndividualActivityDaoBase):
    """
    IndividualActivity に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[IndividualActivity]:
            return db_session.query(IndividualActivity).filter(IndividualActivity.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください