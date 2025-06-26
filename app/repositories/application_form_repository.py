from typing import Optional, Any, List
from sqlalchemy.orm import Session
from app.models.models import ApplicationForm
from app.daos.application_form_dao import ApplicationFormDao
from app.repositories.base.application_form_repository_base import ApplicationFormRepositoryBase

class ApplicationFormRepository(ApplicationFormRepositoryBase):
    """
    ApplicationFormRepositoryBase のカスタムメソッド追加用
    """
    def __init__(self):
        self.dao = ApplicationFormDao()

    def get_by_code(self, db_session: Session, tenant_uuid: str, application_form_code: str) -> ApplicationForm:
        """
        DAO経由で取得
        """
        return self.dao.get_by_code(db_session, tenant_uuid, application_form_code)
