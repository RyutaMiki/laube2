from app.models.models import ApplicationForm
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.application_form_dao_base import ApplicationFormDaoBase

class ApplicationFormDao(ApplicationFormDaoBase):
    """
    ApplicationForm に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ApplicationForm]:
            return db_session.query(ApplicationForm).filter(ApplicationForm.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください