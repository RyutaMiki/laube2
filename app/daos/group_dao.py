from app.models.models import Group
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.group_dao_base import BaseGroupDao


class GroupDao(BaseGroupDao):
    """
    Group に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください