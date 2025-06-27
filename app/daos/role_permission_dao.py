from app.models.models import RolePermission
from sqlalchemy.orm import Session
from typing import Optional
from app.daos.base.role_permission_dao_base import RolePermissionDaoBase

class RolePermissionDao(RolePermissionDaoBase):
    """
    RolePermission に関するカスタムDAO処理クラス。

    ロールとパーミッションの関連付けを管理する。
    トランザクション制御は呼び出し元で行う。
    """

    def add_role_permission(self, db: Session, role_id: str, permission_id: str) -> RolePermission:
        """
        ロールにパーミッションを関連付ける RolePermission を作成する。

        Parameters:
        ----------
        db : Session
            SQLAlchemyセッション（トランザクション制御は呼び出し側）
        role_id : str
            ロールID
        permission_id : str
            パーミッションID

        Returns:
        -------
        RolePermission
            作成された RolePermission エンティティ（commit前）
        """
        entity = RolePermission(role_id=role_id, permission_id=permission_id)
        db.add(entity)
        return entity

    def remove_role_permission(self, db: Session, role_id: str, permission_id: str) -> None:
        """
        ロールとパーミッションの関連付けを削除する。

        Parameters:
        ----------
        db : Session
            SQLAlchemyセッション（トランザクション制御は呼び出し側）
        role_id : str
            ロールID
        permission_id : str
            パーミッションID
        """
        entity = db.query(RolePermission).filter_by(role_id=role_id, permission_id=permission_id).first()
        if entity:
            db.delete(entity)
