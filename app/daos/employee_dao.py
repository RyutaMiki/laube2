from app.models.models import Employee
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.employee_dao_base import BaseEmployeeDao


class EmployeeDao(BaseEmployeeDao):
    """
    Employee に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください