from typing import Optional
from sqlalchemy.orm import Session
from app.daos.user_role_dao import UserRoleDao
from app.models.models import UserRole
from app.repositories.base.user_role_repository_base import UserRoleRepositoryBase


class UserRoleRepository(UserRoleRepositoryBase):
    """
    UserRoleRepositoryBase のカスタムメソッド追加用クラス。

    ユーザーに対するロール割り当て／解除の業務レベル操作を提供。
    """

    def __init__(self):
        super().__init__()
        self.dao = UserRoleDao()

    def assign_role_to_user(self, db: Session, user_id: str, role_id: str) -> UserRole:
        """
        ユーザーにロールを割り当てる。

        Parameters:
        ----------
        db : Session
            SQLAlchemyセッション
        user_id : str
            対象ユーザーID
        role_id : str
            対象ロールID

        Returns:
        -------
        UserRole
            登録された UserRole エンティティ
        """
        return self.dao.add_user_role(db, user_id, role_id)

    def revoke_role_from_user(self, db: Session, user_id: str, role_id: str) -> None:
        """
        ユーザーからロールを解除する。

        Parameters:
        ----------
        db : Session
            SQLAlchemyセッション
        user_id : str
            対象ユーザーID
        role_id : str
            対象ロールID
        """
        self.dao.remove_user_role(db, user_id, role_id)
