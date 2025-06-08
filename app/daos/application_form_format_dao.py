from app.models.models import ApplicationFormFormat
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.application_form_format_dao_base import BaseApplicationFormFormatDao


class ApplicationFormFormatDao(BaseApplicationFormFormatDao):
    """
    ApplicationFormFormat に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください