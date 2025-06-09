from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.application_comment_read_status_repository import ApplicationCommentReadStatusRepository
from app.models.models import ApplicationCommentReadStatus
from app.services.base.base_service import BaseService


class ApplicationCommentReadStatusService(BaseService):
    """
    ApplicationCommentReadStatus に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ApplicationCommentReadStatusRepository] = None):
        self.dao = dao or ApplicationCommentReadStatusRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationCommentReadStatus]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationCommentReadStatus):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ApplicationCommentReadStatus, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ApplicationCommentReadStatus):
        return self.dao.delete(db, instance)