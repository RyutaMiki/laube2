from app.models.models import RolePermission
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.role_permission_dao_base import RolePermissionDaoBase

class RolePermissionDao(RolePermissionDaoBase):
    """
    RolePermission に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[RolePermission]:
            return db_session.query(RolePermission).filter(RolePermission.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください