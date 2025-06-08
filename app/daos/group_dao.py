from app.models.models import Group
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.group_dao_base import GroupDaoBase

class GroupDao(GroupDaoBase):
    """
    Group に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Group]:
            return db_session.query(Group).filter(Group.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください