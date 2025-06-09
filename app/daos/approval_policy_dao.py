from app.models.models import ApprovalPolicy
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.approval_policy_dao_base import ApprovalPolicyDaoBase

class ApprovalPolicyDao(ApprovalPolicyDaoBase):
    """
    ApprovalPolicy に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ApprovalPolicy]:
            return db_session.query(ApprovalPolicy).filter(ApprovalPolicy.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください