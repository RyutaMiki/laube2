from app.models.models import ApplicationClassificationFormat
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.application_classification_format_dao_base import ApplicationClassificationFormatDaoBase

class ApplicationClassificationFormatDao(ApplicationClassificationFormatDaoBase):
    """
    ApplicationClassificationFormat に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ApplicationClassificationFormat]:
            return db_session.query(ApplicationClassificationFormat).filter(ApplicationClassificationFormat.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください