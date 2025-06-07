from jp.co.linkpoint.laube.daos.base.models import Group
from sqlalchemy.orm import Session
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.group_dao_base import BaseGroupDao


class GroupDao(BaseGroupDao):
    """
    Group に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください