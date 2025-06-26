from app.models.models import UserGroup
from sqlalchemy.orm import Session
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
    pass  # 必要に応じてカスタムメソッドをここに追加してください