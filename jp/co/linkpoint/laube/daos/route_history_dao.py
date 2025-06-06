from jp.co.linkpoint.laube.daos.base.models import RouteHistory
from sqlalchemy.orm import Session
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.route_history_dao_base import BaseRouteHistoryDao

class RouteHistoryDao(BaseRouteHistoryDao):
    """
    RouteHistory に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください