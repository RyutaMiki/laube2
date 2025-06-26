from sqlalchemy.orm import Session
from typing import List, Optional, Any
from sqlalchemy.sql import text
from app.models.models import ApplicationForm
from app.daos.base.application_form_dao_base import ApplicationFormDaoBase

class ApplicationFormDao(ApplicationFormDaoBase):
    """
    ApplicationForm に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ApplicationForm]:
            return db_session.query(ApplicationForm).filter(ApplicationForm.name.like(f"%{keyword}%")).all()
    """
    def get_by_code(self, db_session: Session, tenant_uuid: str, application_form_code: str) -> ApplicationForm:
        """
        指定された申請書コードとテナントUUIDに一致する申請書フォームをSQLで取得する。
        """
        sql = text("""
            SELECT * FROM application_forms
            WHERE tenant_uuid = :tenant_uuid
              AND application_form_code = :application_form_code
            LIMIT 1
        """)
        result = db_session.execute(sql, {
            "tenant_uuid": tenant_uuid,
            "application_form_code": application_form_code
        })
        row = result.fetchone()
        return ApplicationForm(**dict(row)) if row else None
