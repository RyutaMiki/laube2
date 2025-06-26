from app.models.models import UserRole
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.user_role_dao_base import UserRoleDaoBase

class UserRoleDao(UserRoleDaoBase):
    """
    UserRole に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[UserRole]:
            return db_session.query(UserRole).filter(UserRole.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください