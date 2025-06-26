from app.models.models import Resource
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.resource_dao_base import ResourceDaoBase

class ResourceDao(ResourceDaoBase):
    """
    Resource に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Resource]:
            return db_session.query(Resource).filter(Resource.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください