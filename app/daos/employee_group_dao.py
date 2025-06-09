from app.models.models import EmployeeGroup
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.employee_group_dao_base import EmployeeGroupDaoBase

class EmployeeGroupDao(EmployeeGroupDaoBase):
    """
    EmployeeGroup に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[EmployeeGroup]:
            return db_session.query(EmployeeGroup).filter(EmployeeGroup.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください