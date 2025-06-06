from jp.co.linkpoint.laube.daos.base.models import ApplicationClassificationFormat
from sqlalchemy.orm import Session
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.application_classification_format_dao_base import BaseApplicationClassificationFormatDao


class ApplicationClassificationFormatDao(BaseApplicationClassificationFormatDao):
    """
    ApplicationClassificationFormat に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください