from app.models.models import Policy
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.policy_dao_base import PolicyDaoBase

class PolicyDao(PolicyDaoBase):
    """
    Policy に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Policy]:
            return db_session.query(Policy).filter(Policy.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください