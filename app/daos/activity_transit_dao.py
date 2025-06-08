from app.models.models import ActivityTransit
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.activity_transit_dao_base import BaseActivityTransitDao


class ActivityTransitDao(BaseActivityTransitDao):
    """
    ActivityTransit に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください