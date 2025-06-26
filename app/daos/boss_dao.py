from app.models.models import Boss
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
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
    def get_by_conditions(self, db: Session, conditions: dict) -> Boss:
        """
        渡された条件dictに基づいて Boss を1件検索する（NULL対応含む）

        :param db: SQLAlchemyのDBセッション
        :param conditions: 検索条件のdict（キー: カラム名, 値: 検索値、None指定で IS NULL）
        :return: BossオブジェクトまたはNone
        """
        where_clauses = []
        params = {}

        for i, (key, value) in enumerate(conditions.items()):
            param_key = f"param_{i}"
            if value is None:
                where_clauses.append(f"{key} IS NULL")
            else:
                where_clauses.append(f"{key} = :{param_key}")
                params[param_key] = value

        sql = text(f"""
            SELECT * FROM boss
            WHERE {' AND '.join(where_clauses)}
            LIMIT 1
        """)

        row = db.execute(sql, params).mappings().first()
        return Boss(**row) if row else None
