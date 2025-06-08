from app.models.models import DeputyApprovel
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.deputy_approvel_dao_base import DeputyApprovelDaoBase

class DeputyApprovelDao(DeputyApprovelDaoBase):
    """
    DeputyApprovel に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[DeputyApprovel]:
            return db_session.query(DeputyApprovel).filter(DeputyApprovel.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください