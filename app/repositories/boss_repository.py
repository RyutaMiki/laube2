from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base.boss_repository_base import BossRepositoryBase
from app.models.models import Boss
from app.daos.boss_dao import BossDao


class BossRepository(BossRepositoryBase):
    """
    BossRepositoryBase のカスタムメソッド追加用クラス。
    データ取得はすべてDAOを通じて行う。
    """
    def __init__(self):
        super().__init__()
        self.dao = BossDao()

    def get_by_all_keys(
        self, db: Session, tenant_uuid: str, group_code: str, user_uuid: str, application_form_code: str
    ) -> Optional[Boss]:
        """
        完全一致キーによる上司マスタ検索。
        """
        return self.dao.get_by_conditions(db, {
            "tenant_uuid": tenant_uuid,
            "group_code": group_code,
            "user_uuid": user_uuid,
            "application_form_code": application_form_code
        })

    def get_by_group_null(
        self, db: Session, tenant_uuid: str, user_uuid: str, application_form_code: str
    ) -> Optional[Boss]:
        """
        group_code が NULL のパターン。
        """
        return self.dao.get_by_conditions(db, {
            "tenant_uuid": tenant_uuid,
            "group_code": None,
            "user_uuid": user_uuid,
            "application_form_code": application_form_code
        })

    def get_by_form_null(
        self, db: Session, tenant_uuid: str, group_code: str, user_uuid: str
    ) -> Optional[Boss]:
        """
        application_form_code が NULL のパターン。
        """
        return self.dao.get_by_conditions(db, {
            "tenant_uuid": tenant_uuid,
            "group_code": group_code,
            "user_uuid": user_uuid,
            "application_form_code": None
        })

    def get_by_group_and_form_null(
        self, db: Session, tenant_uuid: str, user_uuid: str
    ) -> Optional[Boss]:
        """
        group_code と application_form_code が両方 NULL のパターン。
        """
        return self.dao.get_by_conditions(db, {
            "tenant_uuid": tenant_uuid,
            "group_code": None,
            "user_uuid": user_uuid,
            "application_form_code": None
        })
