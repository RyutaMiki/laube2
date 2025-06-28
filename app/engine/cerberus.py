from sqlalchemy.orm import Session
from app.repositories.user_role_repository import UserRoleRepository
from app.repositories.role_permission_repository import RolePermissionRepository
from app.repositories.policy_repository import PolicyRepository

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

    ユーザー・ロール・パーミッション・リソースの関係を管理する。
    Repository経由でトランザクション責務を委譲する。
    """

    def __init__(self):
        self.user_role_repo = UserRoleRepository()
        self.role_permission_repo = RolePermissionRepository()
        self.policy_repo = PolicyRepository()

    def assign_role_to_user(self, db: Session, user_id: str, role_id: str):
        """
        ユーザーにロールを割り当てる。
        """
        return self.user_role_repo.assign_role_to_user(db, user_id, role_id)

    def revoke_role_from_user(self, db: Session, user_id: str, role_id: str):
        """
        ユーザーからロールを解除する。
        """
        self.user_role_repo.revoke_role_from_user(db, user_id, role_id)

    def assign_permission_to_role(self, db: Session, role_id: str, permission_id: str):
        """
        ロールにパーミッションを割り当てる。
        """
        return self.role_permission_repo.assign_permission_to_role(db, role_id, permission_id)

    def revoke_permission_from_role(self, db: Session, role_id: str, permission_id: str):
        """
        ロールからパーミッションを解除する。
        """
        self.role_permission_repo.revoke_permission_from_role(db, role_id, permission_id)

    def assign_resource_to_role(
        self,
        db: Session,
        role_id: str,
        permission_id: str,
        resource_id: str,
        condition: str = None
    ):
        """
        ポリシーを作成して、ロールにリソースとパーミッションを割り当てる。
        事前にrole-permissionに存在しないとエラー。
        """
        if not self.role_permission_repo.has_permission(db, role_id, permission_id):
            raise ValueError(f"Permission {permission_id} is not assigned to Role {role_id}")

        return self.policy_repo.assign_resource_to_role(db, role_id, permission_id, resource_id, condition)

    def revoke_resource_from_role(self, db: Session, role_id: str, permission_id: str, resource_id: str):
        """
        ロールからリソースとパーミッションのポリシーを削除する。
        """
        self.policy_repo.revoke_resource_from_role(db, role_id, permission_id, resource_id)
