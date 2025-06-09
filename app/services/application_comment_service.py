from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.application_comment_repository import ApplicationCommentRepository
from app.models.models import ApplicationComment
from app.services.base.base_service import BaseService


class ApplicationCommentService(BaseService):
    """
    ApplicationComment に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ApplicationCommentRepository] = None):
        self.dao = dao or ApplicationCommentRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationComment]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationComment):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ApplicationComment, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ApplicationComment):
        return self.dao.delete(db, instance)