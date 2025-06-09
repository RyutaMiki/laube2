from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.application_comment_attachment_repository import ApplicationCommentAttachmentRepository
from app.models.models import ApplicationCommentAttachment
from app.services.base.base_service import BaseService


class ApplicationCommentAttachmentService(BaseService):
    """
    ApplicationCommentAttachment に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[ApplicationCommentAttachmentRepository] = None):
        self.dao = dao or ApplicationCommentAttachmentRepository()

    def get(self, db: Session, id: int) -> Optional[ApplicationCommentAttachment]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: ApplicationCommentAttachment):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: ApplicationCommentAttachment, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: ApplicationCommentAttachment):
        return self.dao.delete(db, instance)