from jp.co.linkpoint.laube.daos.base.models import Boss
from sqlalchemy.orm import Session
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.boss_dao_base import BaseBossDao


class BossDao(BaseBossDao):
    """
    Boss に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください