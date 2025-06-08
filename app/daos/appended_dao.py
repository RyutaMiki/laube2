from app.models.models import Appended
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.appended_dao_base import AppendedDaoBase

class AppendedDao(AppendedDaoBase):
    """
    Appended に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Appended]:
            return db_session.query(Appended).filter(Appended.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください