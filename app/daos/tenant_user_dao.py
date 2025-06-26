from sqlalchemy.orm import Session
from app.models.models import TenantUser
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
    def find_active_employee(
        self,
        db_session: Session,
        tenant_uuid: str,
        company_code: str,
        employee_code: str
    ) -> TenantUser | None:
        return db_session.query(TenantUser).filter(
            TenantUser.tenant_uuid == tenant_uuid,
            TenantUser.company_code == company_code,
            TenantUser.employee_code == employee_code,
            TenantUser.is_active.is_(True)
        ).first()
