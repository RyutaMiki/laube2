from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.boss_repository import BossRepository
from app.models.models import Boss
from app.services.base.base_service import BaseService


class BossService(BaseService):
    """
    Boss に対応するサービスクラス。
    ビジネスロジックをここに記述。
    """
    def __init__(self, dao: Optional[BossRepository] = None):
        self.dao = dao or BossRepository()

    def get(self, db: Session, id: int) -> Optional[Boss]:
        return self.dao.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0):
        return self.dao.get_all(db, limit, offset)

    def create(self, db: Session, data: Boss):
        return self.dao.create(db, data)

    def update(self, db: Session, instance: Boss, values: dict):
        return self.dao.update(db, instance, values)

    def delete(self, db: Session, instance: Boss):
        return self.dao.delete(db, instance)