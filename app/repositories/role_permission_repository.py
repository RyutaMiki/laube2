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

    def revoke_permission_from_role(self, db: Session, role_id: str, permission_id: str):
        """
        ロールからパーミッションを解除する。
        policyが関連している場合は削除不可。
        """
        if self.policy_repo.has_policy(db, role_id, permission_id):
            raise ValueError(f"Permission {permission_id} is still used in policies for Role {role_id}")

        self.role_permission_repo.revoke_permission_from_role(db, role_id, permission_id)

    def has_permission(self, db: Session, role_id: str, permission_id: str) -> bool:
        """
        指定されたロールが指定されたパーミッションを保持しているかどうかを返す。
        """
        return db.query(self.model_class).filter_by(
            role_id=role_id,
            permission_id=permission_id
        ).first() is not None
