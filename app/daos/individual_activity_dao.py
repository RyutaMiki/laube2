from sqlalchemy.orm import Session
from app.models.models import IndividualActivity
from typing import List, Optional, Any
from app.daos.base.individual_activity_dao_base import IndividualActivityDaoBase

class IndividualActivityDao(IndividualActivityDaoBase):
    """
    IndividualActivity に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[IndividualActivity]:
            return db_session.query(IndividualActivity).filter(IndividualActivity.name.like(f"%{keyword}%")).all()
    """
    def find_by_tenant_and_route(
        self,
        db_session: Session,
        tenant_uuid: str,
        individual_route_code: str,
        activity_code: str
    ) -> List[IndividualActivity]:
        return db_session.query(IndividualActivity).filter(
            IndividualActivity.tenant_uuid == tenant_uuid,
            IndividualActivity.individual_route_code == individual_route_code,
            IndividualActivity.activity_code == activity_code
        ).all()
