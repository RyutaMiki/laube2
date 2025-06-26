from app.models.models import Role
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.role_dao_base import RoleDaoBase

class RoleDao(RoleDaoBase):
    """
    Role に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Role]:
            return db_session.query(Role).filter(Role.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください