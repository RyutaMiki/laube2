from app.models.models import UserRole
from sqlalchemy.orm import Session
from typing import Optional
from app.daos.base.user_role_dao_base import UserRoleDaoBase

class UserRoleDao(UserRoleDaoBase):
    """
    UserRole に関するカスタムDAO処理クラス。

    ユーザーとロールの関連付けを管理する。
    トランザクション制御は呼び出し元で行う。
    """

    def add_user_role(self, db: Session, user_id: str, role_id: str) -> UserRole:
        """
        ユーザーにロールを割り当てる UserRole エンティティを作成する。

        Parameters:
        ----------
        db : Session
            SQLAlchemyセッション
        user_id : str
            ユーザーID（UUIDなど）
        role_id : str
            ロールID（UUIDなど）

        Returns:
        -------
        UserRole
            作成された UserRole エンティティ（commit前）
        """
        entity = UserRole(user_id=user_id, role_id=role_id)
        db.add(entity)
        return entity

    def remove_user_role(self, db: Session, user_id: str, role_id: str) -> None:
        """
        指定されたユーザーとロールの関連付けを削除する。

        Parameters:
        ----------
        db : Session
            SQLAlchemyセッション
        user_id : str
            ユーザーID
        role_id : str
            ロールID
        """
        entity = db.query(UserRole).filter_by(user_id=user_id, role_id=role_id).first()
        if entity:
            db.delete(entity)
