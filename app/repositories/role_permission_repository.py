# repositories/role_permission_repository.py
from sqlalchemy.orm import Session
from app.models.models import RolePermission
from app.daos.role_permission_dao import RolePermissionDao
from app.repositories.base.role_permission_repository_base import RolePermissionRepositoryBase


class RolePermissionRepository(RolePermissionRepositoryBase):
    """
    RolePermissionRepositoryBase のカスタムメソッド追加用クラス。

    ロールに対するパーミッションの割り当て／解除を行う。
    """

    def __init__(self):
        super().__init__()
        self.dao = RolePermissionDao()

    def assign_permission_to_role(self, db: Session, role_id: str, permission_id: str) -> RolePermission:
        """
        ロールにパーミッションを割り当てる。

        Parameters:
        ----------
        db : Session
            SQLAlchemyセッション
        role_id : str
            対象ロールID
        permission_id : str
            対象パーミッションID

        Returns:
        -------
        RolePermission
            登録された RolePermission エンティティ
        """
        return self.dao.add_role_permission(db, role_id, permission_id)

    def revoke_permission_from_role(self, db: Session, role_id: str, permission_id: str) -> None:
        """
        ロールからパーミッションの割り当てを解除する。

        Parameters:
        ----------
        db : Session
        role_id : str
        permission_id : str
        """
        self.dao.remove_role_permission(db, role_id, permission_id)
