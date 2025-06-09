from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.boss_repository import BossRepository
from app.models.models import Boss
from app.services.base.base_service import BaseService


class BossServiceBase(BaseService):
    """
    Boss に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[BossRepository] = None):
        self.repository = repository or BossRepository()

    def get(self, db: Session, id: int) -> Optional[Boss]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[Boss]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: Boss) -> Boss:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: Boss, data: dict) -> Boss:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: Boss) -> None:
        return self.repository.delete(db, instance)