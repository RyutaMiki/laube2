from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.message_repository import MessageRepository
from app.models.models import Message
from app.services.base.base_service import BaseService


class MessageService(BaseService):
    """
    Message に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[MessageRepository] = None):
        self.dao = dao or MessageRepository()

    def get(self, db: Session, id: int) -> Optional[Message]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Message):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Message, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Message):
        return self.dao.delete(db, instance)