from sqlalchemy.orm import Session
from app.models.models import TenantUser
from typing import List, Optional
from app.daos.base.tenant_user_dao_base import TenantUserDaoBase


class TenantUserDao(TenantUserDaoBase):
    """
    TenantUser に関するカスタムDAO処理を書く場所

    - ユーザー検索など、共通利用されるクエリロジックを記述
    """

    def find_active_user(
        self,
        db_session: Session,
        tenant_uuid: str,
        user_uuid: str
    ) -> Optional[TenantUser]:
        """
        指定されたテナント内でアクティブなユーザーをUUIDで検索する。

        Args:
            db_session (Session): SQLAlchemyのDBセッション
            tenant_uuid (str): テナントUUID
            user_uuid (str): ユーザーUUID

        Returns:
            TenantUser | None: 一致するアクティブユーザー、または None
        """
        return db_session.query(TenantUser).filter(
            TenantUser.tenant_uuid == tenant_uuid,
            TenantUser.user_uuid == user_uuid,
            TenantUser.is_active.is_(True)
        ).first()
