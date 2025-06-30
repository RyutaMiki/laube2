from sqlalchemy.orm import Session
from typing import Optional, Any, List
from app.repositories.base.role_repository_base import RoleRepositoryBase
from app.daos.role_dao import RoleDao
from app.models.models import Role

class RoleRepository(RoleRepositoryBase):
    """
    RoleRepositoryBase のカスタムメソッド追加用
    """
    def __init__(self):
        self.role_dao = RoleDao()

    def find_by_code(
        self,
        db_session: Session,
        tenant_uuid: str,
        approverl_tenant_uuid: str,
        role_code: str
    ) -> Optional[Role]:
        """
        指定されたロールコードに一致するロールを取得する。

        Args:
            db_session (Session): SQLAlchemyのセッション
            tenant_uuid (str): 呼び出し元テナントUUID（管理テナント）
            approverl_tenant_uuid (str): ロールの所属テナント（承認者側）
            role_code (str): ロールコード

        Returns:
            Optional[Role]: 一致するロール、存在しなければ None
        """
        return self.role_dao.get_by_code(
            db_session=db_session,
            tenant_uuid=tenant_uuid,
            approverl_tenant_uuid=approverl_tenant_uuid,
            role_code=role_code
        )