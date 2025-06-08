from app.models.models import ApplicationObject
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.application_object_dao_base import BaseApplicationObjectDao


class ApplicationObjectDao(BaseApplicationObjectDao):
    """
    ApplicationObject に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください