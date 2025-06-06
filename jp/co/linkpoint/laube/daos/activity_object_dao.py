from jp.co.linkpoint.laube.daos.base.models import ActivityObject
from sqlalchemy.orm import Session
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.activity_object_dao_base import BaseActivityObjectDao

class ActivityObjectDao(BaseActivityObjectDao):
    """
    ActivityObject に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください