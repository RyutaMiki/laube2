from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class BaseDao(Generic[T]):
    """
    共通DAO基底クラス
    """

    model = None  # 継承先で必ずセットする

    def get_by_key(self, db_session: Session, id: int) -> List[T]:
        query = db_session.query(self.model)
        if id is not None:
            query = query.filter(self.model.id == id)
        return query.all()

    def insert(self, db_session: Session, instance: T) -> T:
        db_session.add(instance)
        db_session.flush()
        return instance

    def delete(self, db_session: Session, instance: T) -> None:
        db_session.delete(instance)
        db_session.flush()

    def get_all(self, db_session: Session, limit: int = 100, offset: int = 0) -> List[T]:
        return db_session.query(self.model).limit(limit).offset(offset).all()

    def count(self, db_session: Session) -> int:
        return db_session.query(func.count()).select_from(self.model).scalar()

    def update(self, db_session: Session, id: int, update_data: dict) -> Optional[T]:
        results = self.get_by_key(db_session, id=id)
        instance = results[0] if results else None
        if instance:
            for key, value in update_data.items():
                setattr(instance, key, value)
            db_session.add(instance)
        db_session.flush()
        return instance
