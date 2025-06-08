from app.models.models import ApplicationFormRoute
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.application_form_route_dao_base import ApplicationFormRouteDaoBase

class ApplicationFormRouteDao(ApplicationFormRouteDaoBase):
    """
    ApplicationFormRoute に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ApplicationFormRoute]:
            return db_session.query(ApplicationFormRoute).filter(ApplicationFormRoute.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください