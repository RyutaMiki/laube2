from app.models.models import Policy
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from app.daos.base.policy_dao_base import PolicyDaoBase

class PolicyDao(PolicyDaoBase):
    """
    Policy に関するカスタムDAO処理クラス。

    このクラスでは、Policyエンティティの追加・削除処理を提供する。
    トランザクション制御（commit/rollback）は呼び出し元に委譲し、ここでは実行しない。
    """

    def add_policy(self, db: Session, role_id: str, permission_id: str, resource_id: str, condition: Optional[str] = None) -> Policy:
        """
        Policy エンティティを作成してDBに追加（flush対象に追加）する。

        Parameters:
        ----------
        db : Session
            SQLAlchemyセッション（トランザクション制御は呼び出し側）
        role_id : str
            ロールID
        permission_id : str
            パーミッションID
        resource_id : str
            リソースID
        condition : Optional[str]
            アクセス条件（JSONや式）

        Returns:
        -------
        Policy
            作成された Policy オブジェクト（まだ commit はされていない）
        """
        entity = Policy(
            policy_id=str(uuid.uuid4()),
            role_id=role_id,
            permission_id=permission_id,
            resource_id=resource_id,
            condition=condition
        )
        db.add(entity)
        return entity

    def remove_policy(self, db: Session, role_id: str, permission_id: str, resource_id: str) -> None:
        """
        指定されたロール・パーミッション・リソースに一致する Policy を削除する。

        Parameters:
        ----------
        db : Session
            SQLAlchemyセッション（トランザクション制御は呼び出し側）
        role_id : str
            ロールID
        permission_id : str
            パーミッションID
        resource_id : str
            リソースID
        """
        entity = db.query(Policy).filter_by(
            role_id=role_id,
            permission_id=permission_id,
            resource_id=resource_id
        ).first()
        if entity:
            db.delete(entity)
