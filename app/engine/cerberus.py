from sqlalchemy.orm import Session
from app.daos.user_role_dao import UserRoleDao
from app.daos.role_permission_dao import RolePermissionDao
from app.daos.policy_dao import PolicyDao


######################################################################
# Copyright 2016–2025 Ryuta Miki. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################


class Cerberus:
    """
    Cerberus（ケルベロス）アクセス制御エンジン。

    このクラスは、ユーザー・ロール・パーミッション・リソースの関係を管理し、
    アクセス制御の中心的な操作（追加・削除）を提供する。

    セッションは外部から注入され、内部で管理は行わない。
    """

    def __init__(self):
        """
        Cerberusエンジンを初期化する。
        各種DAOをインスタンス化する。
        """
        self.user_role_dao = UserRoleDao()
        self.role_permission_dao = RolePermissionDao()
        self.policy_dao = PolicyDao()

    def assign_role_to_user(self, db: Session, user_id: str, role_id: str):
        """
        ユーザーにロールを割り当てる。

        :param db: SQLAlchemyセッション
        :param user_id: 対象ユーザーID（UUID）
        :param role_id: 割り当てるロールID（UUID）
        :return: 作成された UserRole エンティティ
        """
        return self.user_role_dao.add_user_role(db, user_id, role_id)

    def revoke_role_from_user(self, db: Session, user_id: str, role_id: str):
        """
        ユーザーからロールの割り当てを削除する。

        :param db: SQLAlchemyセッション
        :param user_id: 対象ユーザーID（UUID）
        :param role_id: 削除するロールID（UUID）
        """
        self.user_role_dao.remove_user_role(db, user_id, role_id)

    def assign_permission_to_role(self, db: Session, role_id: str, permission_id: str):
        """
        ロールにパーミッションを割り当てる。

        :param db: SQLAlchemyセッション
        :param role_id: 対象ロールID（UUID）
        :param permission_id: 割り当てるパーミッションID（UUID）
        :return: 作成された RolePermission エンティティ
        """
        return self.role_permission_dao.add_role_permission(db, role_id, permission_id)

    def revoke_permission_from_role(self, db: Session, role_id: str, permission_id: str):
        """
        ロールからパーミッションの割り当てを削除する。

        :param db: SQLAlchemyセッション
        :param role_id: 対象ロールID（UUID）
        :param permission_id: 削除するパーミッションID（UUID）
        """
        self.role_permission_dao.remove_role_permission(db, role_id, permission_id)

    def assign_resource_to_role(self, db: Session, role_id: str, permission_id: str, resource_id: str, condition: str = None):
        """
        ポリシーを作成し、ロールにリソースとパーミッションを割り当てる。

        :param db: SQLAlchemyセッション
        :param role_id: 対象ロールID（UUID）
        :param permission_id: 対象パーミッションID（UUID）
        :param resource_id: 対象リソースID（UUID）
        :param condition: オプションのアクセス条件（JSONまたは式）
        :return: 作成された Policy エンティティ
        """
        return self.policy_dao.add_policy(db, role_id, permission_id, resource_id, condition)

    def revoke_resource_from_role(self, db: Session, role_id: str, permission_id: str, resource_id: str):
        """
        ロールから指定されたリソースとパーミッションに関するポリシーを削除する。

        :param db: SQLAlchemyセッション
        :param role_id: 対象ロールID（UUID）
        :param permission_id: 対象パーミッションID（UUID）
        :param resource_id: 対象リソースID（UUID）
        """
        self.policy_dao.remove_policy(db, role_id, permission_id, resource_id)
