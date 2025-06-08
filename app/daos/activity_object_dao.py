from app.models.models import ActivityObject
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.activity_object_dao_base import ActivityObjectDaoBase

class ActivityObjectDao(ActivityObjectDaoBase):
    """
    ActivityObject に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ActivityObject]:
            return db_session.query(ActivityObject).filter(ActivityObject.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください