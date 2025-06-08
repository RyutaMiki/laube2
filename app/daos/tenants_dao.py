from app.models.models import Tenants
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.tenants_dao_base import TenantsDaoBase

class TenantsDao(TenantsDaoBase):
    """
    Tenants に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Tenants]:
            return db_session.query(Tenants).filter(Tenants.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください