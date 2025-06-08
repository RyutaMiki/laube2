from app.models.models import DeputyApprovel
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.deputy_approvel_dao_base import BaseDeputyApprovelDao


class DeputyApprovelDao(BaseDeputyApprovelDao):
    """
    DeputyApprovel に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください