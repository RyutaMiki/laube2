from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Union, Any
from app.daos.base_dao import BaseDao
from app.models.models import Employee

from datetime import datetime, date

class BaseEmployeeDao(BaseDao[Employee]):
    """
    Data Access Object for Employee.
    """
    model = Employee

    def create(self, db_session: Session, data: Union[Employee, dict]) -> Employee:
        """
        Employee を登録します。

        Args:
            db_session (Session): DBセッション
            data (Employee or dict): 保存するインスタンスまたは dict

        Returns:
            Employee: 保存後のインスタンス
        """
        try:
            if isinstance(data, dict):
                instance = Employee(**data)
            else:
                instance = data
            db_session.add(instance)
            db_session.flush()
            return instance
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"[DAO.create] 登録に失敗: {e}") from e

    def delete(self, db_session: Session, instance: Employee) -> None:
        """
        Employee を削除します。

        Args:
            db_session (Session): DBセッション
            instance (Employee): 削除するインスタンス

        Returns:
            None
        """
        try:
            db_session.delete(instance)
            db_session.flush()
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"[DAO.delete] 削除に失敗: {e}") from e

    def get_by_key(self, db_session: Session, id: int) -> List[Employee]:
        """
        Employee を指定された主キー条件で取得します。

        Args:
            db_session (Session): DBセッション
            id (Optional[int]): サロゲートキー

        Returns:
            List[Employee]: 条件に一致するレコードのリスト
        """
        query = db_session.query(Employee)
        if id is not None:
            query = query.filter(Employee.id == id)
        return query.all()

    def get(self, db_session: Session, id: int) -> Optional[Employee]:
        """
        主キーで単一取得。

        Returns:
            Optional[Employee]: 該当するインスタンス or None
        """
        result = self.get_by_key(db_session, id=id)
        return result[0] if result else None

    def get_all(self, db_session: Session, limit: int = 100, offset: int = 0) -> List[Employee]:
        """
        全件取得（ページング対応）

        Returns:
            List[Employee]
        """
        return db_session.query(Employee).limit(limit).offset(offset).all()

    def count(self, db_session: Session) -> int:
        """
        総件数カウント

        Returns:
            int
        """
        return db_session.query(func.count()).select_from(Employee).scalar()

    def update(self, db_session: Session, id: int, update_data: dict) -> Optional[Employee]:
        """
        主キー一致した1件をupdate（更新フィールドはdict）

        Returns:
            Optional[Employee]: 更新後インスタンス or None
        """
        results = self.get_by_key(db_session, id=id)
        instance = results[0] if results else None
        if instance:
            for key, value in update_data.items():
                setattr(instance, key, value)
            db_session.add(instance)
            db_session.flush()
        return instance