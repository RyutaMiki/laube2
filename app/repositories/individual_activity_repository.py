from sqlalchemy.orm import Session
from typing import List
from app.models.models import IndividualActivity
from app.repositories.base.individual_activity_repository_base import IndividualActivityRepositoryBase
from app.daos.individual_activity_dao import IndividualActivityDao 


class IndividualActivityRepository(IndividualActivityRepositoryBase):
    """
    IndividualActivityRepositoryBase のカスタムメソッド追加用リポジトリクラス。
    """

    def __init__(self):
        super().__init__()
        self.dao = IndividualActivityDao()

    def find_by_tenant_and_route(
        self,
        db_session: Session,
        tenant_uuid: str,
        individual_route_code: str,
        activity_code: str
    ) -> List[IndividualActivity]:
        return self.dao.find_by_tenant_and_route(
            db_session,
            tenant_uuid,
            individual_route_code,
            activity_code
        )