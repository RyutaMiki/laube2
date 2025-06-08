from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Union, Any
from app.daos.base.base_dao import BaseDao
from app.models.models import Employee

from datetime import datetime, date

class EmployeeDaoBase(BaseDao[Employee]):
    """
    Data Access Object for Employee.
    """
    model = Employee

    def create(
        self,
        db_session: Session,
        data: Union[Employee, dict]
    ) -> Employee:
        """
        Employee を登録します。
        """
        try:
            instance = Employee(**data) if isinstance(data, dict) else data
            db_session.add(instance)
            db_session.flush()
            return instance
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"[DAO.create] 登録に失敗: {e}") from e

    def delete(
        self,
        db_session: Session,
        instance: Employee
    ) -> None:
        """
        Employee を削除します。
        """
        try:
            db_session.delete(instance)
            db_session.flush()
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"[DAO.delete] 削除に失敗: {e}") from e

    def get_by_key(
        self,
        db_session: Session,
        id: Optional[int]    ) -> List[Employee]:
        """
        Employee を主キー条件で取得します。
        """
        query = db_session.query(Employee)
        if id is not None:
            query = query.filter(Employee.id == id)
        return query.all()

    def get(
        self,
        db_session: Session,
        id: Optional[int]    ) -> Optional[Employee]:
        """
        主キーで単一取得。
        """
        result = self.get_by_key(
            db_session
, id=id        )
        return result[0] if result else None

    def get_all(
        self,
        db_session: Session,
        limit: int = 100,
        offset: int = 0
    ) -> List[Employee]:
        """
        全件取得（ページング対応）
        """
        return db_session.query(Employee).limit(limit).offset(offset).all()

    def count(
        self,
        db_session: Session
    ) -> int:
        """
        総件数カウント
        """
        return db_session.query(func.count()).select_from(Employee).scalar()

    def update(
        self,
        db_session: Session,
        id: Optional[int],
        update_data: dict
    ) -> Optional[Employee]:
        """
        主キー一致した1件をupdate（更新フィールドはdict）
        """
        results = self.get_by_key(
            db_session
, id=id        )
        instance = results[0] if results else None
        if instance:
            for key, value in update_data.items():
                setattr(instance, key, value)
            db_session.add(instance)
            db_session.flush()
        return instance