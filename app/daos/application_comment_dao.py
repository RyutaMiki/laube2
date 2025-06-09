from app.models.models import ApplicationComment
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.application_comment_dao_base import ApplicationCommentDaoBase

class ApplicationCommentDao(ApplicationCommentDaoBase):
    """
    ApplicationComment に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ApplicationComment]:
            return db_session.query(ApplicationComment).filter(ApplicationComment.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください