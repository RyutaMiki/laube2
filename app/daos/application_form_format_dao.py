from app.models.models import ApplicationFormFormat
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.application_form_format_dao_base import ApplicationFormFormatDaoBase

class ApplicationFormFormatDao(ApplicationFormFormatDaoBase):
    """
    ApplicationFormFormat に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ApplicationFormFormat]:
            return db_session.query(ApplicationFormFormat).filter(ApplicationFormFormat.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください