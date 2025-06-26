from sqlalchemy.orm import Session
from app.models.models import UserGroup
from typing import List, Optional, Any
from app.daos.base.user_group_dao_base import UserGroupDaoBase

class UserGroupDao(UserGroupDaoBase):
    """
    UserGroup に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[UserGroup]:
            return db_session.query(UserGroup).filter(UserGroup.name.like(f"%{keyword}%")).all()
    """
    def find_by_keys(
        self,
        db_session: Session,
        tenant_uuid: str,
        company_code: str,
        employee_code: str,
        group_code: str
    ) -> UserGroup | None:
        return db_session.query(UserGroup).filter(
            UserGroup.tenant_uuid == tenant_uuid,
            UserGroup.company_code == company_code,
            UserGroup.employee_code == employee_code,
            UserGroup.group_code == group_code
        ).first()
