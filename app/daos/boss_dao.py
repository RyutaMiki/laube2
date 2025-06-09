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
    def get_by_conditions(self, db: Session, conditions: dict) -> Optional[Boss]:
        """
        dictで渡された条件で単一レコードを検索する共通関数。
        """
        query = db.query(self.model)
        for attr, value in conditions.items():
            if value is None:
                query = query.filter(getattr(self.model, attr) == None)
            else:
                query = query.filter(getattr(self.model, attr) == value)
        return query.first()

    pass  # 必要に応じてカスタムメソッドをここに追加してください