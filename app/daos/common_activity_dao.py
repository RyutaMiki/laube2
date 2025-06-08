from app.models.models import CommonActivity
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.common_activity_dao_base import BaseCommonActivityDao


class CommonActivityDao(BaseCommonActivityDao):
    """
    CommonActivity に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください