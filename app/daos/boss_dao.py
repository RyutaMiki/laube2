from app.models.models import Boss
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.boss_dao_base import BossDaoBase

class BossDao(BossDaoBase):
    """
    Boss に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Boss]:
            return db_session.query(Boss).filter(Boss.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください