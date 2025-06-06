from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.base_dao import BaseDao
from jp.co.linkpoint.laube.daos.base.models import IndividualRoute

from datetime import datetime

class BaseIndividualRouteDao(BaseDao[IndividualRoute]):
    """
    Data Access Object for IndividualRoute.
    """
    model = IndividualRoute

    def get_by_key(self, db_session: Session, id: int) -> List[IndividualRoute]:
        """
        IndividualRoute を指定された主キー条件であいまい取得します。

        Args:
            db_session (Session): DBセッション
            id (Optional[int]): サロゲートキー（指定された場合のみ条件に含めます）

        Returns:
            List[IndividualRoute]: 条件に一致するレコードのリスト
        """
        query = db_session.query(IndividualRoute)
        if id is not None:
            query = query.filter(IndividualRoute.id == id)
        return query.all()

    def insert(self, db_session: Session, instance: IndividualRoute) -> IndividualRoute:
        """
        IndividualRoute を登録します。

        Args:
            db_session (Session): DBセッション
            instance (IndividualRoute): 保存するインスタンス

        Returns:
            IndividualRoute: 保存後のインスタンス
        """
        db_session.add(instance)
        db_session.flush()
        return instance

    def delete(self, db_session: Session, instance: IndividualRoute) -> None:
        """
        IndividualRoute を削除します。

        Args:
            db_session (Session): DBセッション
            instance (IndividualRoute): 削除するインスタンス

        Returns:
            None
        """
        db_session.delete(instance)
        db_session.flush()

    def get_all(self, db_session: Session, limit: int = 100, offset: int = 0) -> List[IndividualRoute]:
        """
        IndividualRoute を全件取得します（ページング対応）。

        Args:
            db_session (Session): DBセッション
            limit (int): 最大取得件数
            offset (int): 取得開始位置

        Returns:
            List[IndividualRoute]: 取得されたインスタンスのリスト
        """
        return db_session.query(IndividualRoute).limit(limit).offset(offset).all()

    def count(self, db_session: Session) -> int:
        """
        IndividualRoute の総件数を取得します。

        Args:
            db_session (Session): DBセッション

        Returns:
            int: 件数
        """
        return db_session.query(func.count()).select_from(IndividualRoute).scalar()

    def update(self, db_session: Session, id: int, update_data: dict) -> Optional[IndividualRoute]:
        """
        指定された主キーに一致する IndividualRoute を更新します。

        Args:
            db_session (Session): DBセッション
            id (int): サロゲートキー
            update_data (dict): 更新内容の辞書

        Returns:
            Optional[IndividualRoute]: 更新後のインスタンスまたは None
        """
        results = self.get_by_key(db_session, id=id)
        instance = results[0] if results else None

        if instance:
            for key, value in update_data.items():
                setattr(instance, key, value)
            db_session.add(instance)

        db_session.flush()
        return instance