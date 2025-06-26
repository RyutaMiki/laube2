from sqlalchemy.orm import Session
from typing import Optional, Any, List
from app.models.models import ApplicationFormRoute
from app.daos.application_form_route_dao import ApplicationFormRouteDao
from app.repositories.base.application_form_route_repository_base import ApplicationFormRouteRepositoryBase


class ApplicationFormRouteRepository(ApplicationFormRouteRepositoryBase):
    """
    ApplicationFormRouteRepositoryBase のカスタムメソッド追加用
    """
    def __init__(self):
        self.dao = ApplicationFormRouteDao()

    def get_by_code_and_group(self, db_session: Session, tenant_uuid: str, application_form_code: str, group_code: str) -> ApplicationFormRoute:
        """
        DAOを経由して申請ルートを取得する
        """
        return self.dao.get_by_code_and_group(db_session, tenant_uuid, application_form_code, group_code)
