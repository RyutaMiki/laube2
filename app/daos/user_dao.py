from app.models.models import User
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.user_dao_base import UserDaoBase

class UserDao(UserDaoBase):
    """
    User に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[User]:
            return db_session.query(User).filter(User.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください