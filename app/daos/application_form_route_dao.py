from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List, Optional, Any
from app.models.models import ApplicationFormRoute
from app.daos.base.application_form_route_dao_base import ApplicationFormRouteDaoBase

class ApplicationFormRouteDao(ApplicationFormRouteDaoBase):
    """
    ApplicationFormRoute に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ApplicationFormRoute]:
            return db_session.query(ApplicationFormRoute).filter(ApplicationFormRoute.name.like(f"%{keyword}%")).all()
    """
    def get_by_code_and_group(self, db_session: Session, tenant_uuid: str, application_form_code: str, group_code: str) -> ApplicationFormRoute:
        """
        テナントUUID・申請書コード・グループコードに一致するルートを取得する
        """
        sql = text("""
            SELECT * FROM application_form_routes
            WHERE tenant_uuid = :tenant_uuid
              AND application_form_code = :application_form_code
              AND group_code = :group_code
            LIMIT 1
        """)
        row = db_session.execute(sql, {
            "tenant_uuid": tenant_uuid,
            "application_form_code": application_form_code,
            "group_code": group_code
        }).mappings().first()

        return ApplicationFormRoute(**row) if row else None
