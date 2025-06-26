from app.models.models import Permission
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.permission_dao_base import PermissionDaoBase

class PermissionDao(PermissionDaoBase):
    """
    Permission に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Permission]:
            return db_session.query(Permission).filter(Permission.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください