from app.models.models import Tenant
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.tenant_dao_base import TenantDaoBase

class TenantDao(TenantDaoBase):
    """
    Tenant に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Tenant]:
            return db_session.query(Tenant).filter(Tenant.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください