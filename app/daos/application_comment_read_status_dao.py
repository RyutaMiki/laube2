from app.models.models import ApplicationCommentReadStatus
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.application_comment_read_status_dao_base import ApplicationCommentReadStatusDaoBase

class ApplicationCommentReadStatusDao(ApplicationCommentReadStatusDaoBase):
    """
    ApplicationCommentReadStatus に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[ApplicationCommentReadStatus]:
            return db_session.query(ApplicationCommentReadStatus).filter(ApplicationCommentReadStatus.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください