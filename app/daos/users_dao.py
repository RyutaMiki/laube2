from app.models.models import Users
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.users_dao_base import UsersDaoBase

class UsersDao(UsersDaoBase):
    """
    Users に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Users]:
            return db_session.query(Users).filter(Users.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください