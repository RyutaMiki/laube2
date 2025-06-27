# repositories/policy_repository.py
from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import Policy
from app.daos.policy_dao import PolicyDao
from app.repositories.base.policy_repository_base import PolicyRepositoryBase


class PolicyRepository(PolicyRepositoryBase):
    """
    PolicyRepositoryBase のカスタムメソッド追加用クラス。

    ロールに対するリソース＋パーミッションの関連（ポリシー）管理。
    """

    def __init__(self):
        super().__init__()
        self.dao = PolicyDao()

    def assign_resource_to_role(self, db: Session, role_id: str, permission_id: str, resource_id: str, condition: Optional[str] = None) -> Policy:
        """
        ロールに対してリソース×パーミッションのアクセスポリシーを割り当てる。

        Parameters:
        ----------
        db : Session
        role_id : str
        permission_id : str
        resource_id : str
        condition : Optional[str]
            オプションの条件式（JSON等）

        Returns:
        -------
        Policy
            登録された Policy エンティティ
        """
        return self.dao.add_policy(db, role_id, permission_id, resource_id, condition)

    def revoke_resource_from_role(self, db: Session, role_id: str, permission_id: str, resource_id: str) -> None:
        """
        ロールに割り当てられたリソース×パーミッションのポリシーを削除する。

        Parameters:
        ----------
        db : Session
        role_id : str
        permission_id : str
        resource_id : str
        """
        self.dao.remove_policy(db, role_id, permission_id, resource_id)
