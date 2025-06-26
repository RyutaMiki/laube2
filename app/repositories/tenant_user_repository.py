from sqlalchemy.orm import Session
from app.daos.tenant_user_dao import TenantUserDao
from app.models.models import TenantUser
from typing import Optional, Any, List
from app.repositories.base.tenant_user_repository_base import TenantUserRepositoryBase

class TenantUserRepository(TenantUserRepositoryBase):
    """
    TenantUserRepositoryBase のカスタムメソッド追加用
    """
    def __init__(self):
        self.dao = TenantUserDao()

    def find_active_user(
        self,
        db_session: Session,
        tenant_uuid: str,
        user_uuid: str
    ) -> Optional[TenantUser]:
        return db_session.query(TenantUser).filter(
            TenantUser.tenant_uuid == tenant_uuid,
            TenantUser.user_uuid == user_uuid,
            TenantUser.belong_end_date.is_(None)
        ).first()
