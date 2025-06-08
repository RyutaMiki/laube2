from app.models.models import Appended
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.appended_dao_base import BaseAppendedDao


class AppendedDao(BaseAppendedDao):
    """
    Appended に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください