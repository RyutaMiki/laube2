from app.models.models import TenantUser
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.tenant_user_dao_base import TenantUserDaoBase

class TenantUserDao(TenantUserDaoBase):
    """
    TenantUser に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[TenantUser]:
            return db_session.query(TenantUser).filter(TenantUser.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください