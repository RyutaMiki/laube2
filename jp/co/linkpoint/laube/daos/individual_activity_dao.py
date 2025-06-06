from jp.co.linkpoint.laube.daos.base.models import IndividualActivity
from sqlalchemy.orm import Session
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.individual_activity_dao_base import BaseIndividualActivityDao


class IndividualActivityDao(BaseIndividualActivityDao):
    """
    IndividualActivity に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください