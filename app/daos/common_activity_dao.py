from app.models.models import CommonActivity
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.common_activity_dao_base import CommonActivityDaoBase

class CommonActivityDao(CommonActivityDaoBase):
    """
    CommonActivity に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[CommonActivity]:
            return db_session.query(CommonActivity).filter(CommonActivity.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください