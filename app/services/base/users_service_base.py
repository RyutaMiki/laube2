from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.users_repository import UsersRepository
from app.models.models import Users
from app.services.base.base_service import BaseService


class UsersServiceBase(BaseService):
    """
    Users に関する基本的なサービス処理（BaseService継承）
    """
    def __init__(self, repository: Optional[UsersRepository] = None):
        self.repository = repository or UsersRepository()

    def get(self, db: Session, id: int) -> Optional[Users]:
        return self.repository.get(db, id)

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[Users]:
        return self.repository.get_all(db, limit, offset)

    def create(self, db: Session, data: Users) -> Users:
        return self.repository.create(db, data)

    def update(self, db: Session, instance: Users, data: dict) -> Users:
        return self.repository.update(db, instance, data)

    def delete(self, db: Session, instance: Users) -> None:
        return self.repository.delete(db, instance)