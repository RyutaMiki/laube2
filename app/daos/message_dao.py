from app.models.models import Message
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from app.daos.base.message_dao_base import MessageDaoBase

class MessageDao(MessageDaoBase):
    """
    Message に関するカスタムDAO処理を書く場所

    - サンプルメソッドをここに追加できます。
    - 例:
        def custom_search(self, db_session: Session, keyword: str) -> List[Message]:
            return db_session.query(Message).filter(Message.name.like(f"%{keyword}%")).all()
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください