from jp.co.linkpoint.laube.daos.base.models import CommonRoute
from sqlalchemy.orm import Session
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.common_route_dao_base import BaseCommonRouteDao

class CommonRouteDao(BaseCommonRouteDao):
    """
    CommonRoute に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください