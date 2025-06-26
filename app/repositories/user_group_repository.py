from sqlalchemy.orm import Session
from app.daos.user_group_dao import UserGroupDao
from app.models.models import UserGroup
from typing import Optional, Any, List
from app.repositories.base.user_group_repository_base import UserGroupRepositoryBase

class UserGroupRepository(UserGroupRepositoryBase):
    """
    UserGroupRepositoryBase のカスタムメソッド追加用
    """
    def __init__(self):
        self.dao = UserGroupDao()

    def find_by_keys(self, db_session, tenant_uuid: str, user_uuid: str, group_code: str) -> Optional[UserGroup]:
        return db_session.query(UserGroup).filter_by(
            tenant_uuid=tenant_uuid,
            user_uuid=user_uuid,
            group_code=group_code
        ).first()