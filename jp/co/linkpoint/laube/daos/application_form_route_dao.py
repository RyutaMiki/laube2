from jp.co.linkpoint.laube.daos.base.models import ApplicationFormRoute
from sqlalchemy.orm import Session
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.application_form_route_dao_base import BaseApplicationFormRouteDao


class ApplicationFormRouteDao(BaseApplicationFormRouteDao):
    """
    ApplicationFormRoute に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください