from app.models.models import Role
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.role_dao_base import RoleDaoBase


class RoleDao(RoleDaoBase):
    """
    Role に関するカスタムDAO処理を書く場所。

    通常は Repository で十分だが、複雑なJOINや条件付き取得を行う場合はDAOに記述する。
    """
    def get_by_code(
        self,
        db_session: Session,
        tenant_uuid: str,
        approverl_tenant_uuid: str,
        role_code: str
    ) -> Optional[Role]:
        """
        指定されたロールコードに一致するロールを取得する。

        Args:
            db_session (Session): DBセッション
            tenant_uuid (str): 呼び出し元テナント（管理対象）
            approverl_tenant_uuid (str): 承認者の所属テナント
            role_code (str): ロールコード

        Returns:
            Optional[Role]: 一致するロール、なければ None
        """
        return db_session.query(Role).filter(
            Role.tenant_uuid == tenant_uuid,
            Role.company_uuid == approverl_tenant_uuid,
            Role.role_code == role_code,
            Role.is_active.is_(True)
        ).first()

    def get_active_roles_by_tenant(
        self,
        db_session: Session,
        tenant_uuid: str
    ) -> List[Role]:
        """
        指定されたテナントの全アクティブなロールを取得する。

        Args:
            db_session (Session): SQLAlchemyのDBセッション
            tenant_uuid (str): テナントUUID

        Returns:
            List[Role]: 該当するロールリスト
        """
        return db_session.query(Role).filter(
            Role.tenant_uuid == tenant_uuid,
            Role.is_active.is_(True)
        ).all()

    def search_by_keyword(
        self,
        db_session: Session,
        tenant_uuid: str,
        keyword: str
    ) -> List[Role]:
        """
        ロール名またはコードにキーワードが含まれるロールを検索する。

        Args:
            db_session (Session): SQLAlchemyのDBセッション
            tenant_uuid (str): テナントUUID
            keyword (str): 部分一致検索キーワード

        Returns:
            List[Role]: 該当ロール
        """
        return db_session.query(Role).filter(
            Role.tenant_uuid == tenant_uuid,
            Role.is_active.is_(True),
            (
                Role.role_code.ilike(f"%{keyword}%") |
                Role.role_name.ilike(f"%{keyword}%")
            )
        ).all()

    def get_role_by_user_uuid(
        self,
        db_session: Session,
        tenant_uuid: str,
        user_uuid: str
    ) -> List[Role]:
        """
        ユーザーに関連付けられたロール一覧を取得する（中間テーブルJOIN前提）

        Args:
            db_session (Session): DBセッション
            tenant_uuid (str): テナントUUID
            user_uuid (str): ユーザーUUID

        Returns:
            List[Role]: 関連ロール（UserRoleなどとのJOINが必要）
        """
        # 仮に user_roles テーブルが存在すると仮定
        return (
            db_session.query(Role)
            .join(Role.user_roles)  # Relationship定義されてる前提
            .filter(
                Role.tenant_uuid == tenant_uuid,
                Role.is_active.is_(True),
                Role.user_roles.any(user_uuid=user_uuid)
            )
            .all()
        )
