from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.base_dao import BaseDao
from jp.co.linkpoint.laube.daos.base.models import ApplicationFormRoute

from datetime import datetime


class BaseApplicationFormRouteDao(BaseDao[ApplicationFormRoute]):
    """
    Data Access Object for ApplicationFormRoute.
    """
    model = ApplicationFormRoute

    def get_by_key(self, db_session: Session, id: int) -> List[ApplicationFormRoute]:
        """
        ApplicationFormRoute を指定された主キー条件であいまい取得します。

        Args:
            db_session (Session): DBセッション
            id (Optional[int]): サロゲートキー（指定された場合のみ条件に含めます）

        Returns:
            List[ApplicationFormRoute]: 条件に一致するレコードのリスト
        """
        query = db_session.query(ApplicationFormRoute)
        if id is not None:
            query = query.filter(ApplicationFormRoute.id == id)
        return query.all()

    def insert(self, db_session: Session, instance: ApplicationFormRoute) -> ApplicationFormRoute:
        """
        ApplicationFormRoute を登録します。

        Args:
            db_session (Session): DBセッション
            instance (ApplicationFormRoute): 保存するインスタンス

        Returns:
            ApplicationFormRoute: 保存後のインスタンス
        """
        db_session.add(instance)
        db_session.flush()
        return instance

    def delete(self, db_session: Session, instance: ApplicationFormRoute) -> None:
        """
        ApplicationFormRoute を削除します。

        Args:
            db_session (Session): DBセッション
            instance (ApplicationFormRoute): 削除するインスタンス

        Returns:
            None
        """
        db_session.delete(instance)
        db_session.flush()

    def get_all(self, db_session: Session, limit: int = 100, offset: int = 0) -> List[ApplicationFormRoute]:
        """
        ApplicationFormRoute を全件取得します（ページング対応）。

        Args:
            db_session (Session): DBセッション
            limit (int): 最大取得件数
            offset (int): 取得開始位置

        Returns:
            List[ApplicationFormRoute]: 取得されたインスタンスのリスト
        """
        return db_session.query(ApplicationFormRoute).limit(limit).offset(offset).all()

    def count(self, db_session: Session) -> int:
        """
        ApplicationFormRoute の総件数を取得します。

        Args:
            db_session (Session): DBセッション

        Returns:
            int: 件数
        """
        return db_session.query(func.count()).select_from(ApplicationFormRoute).scalar()

    def update(self, db_session: Session, id: int, update_data: dict) -> Optional[ApplicationFormRoute]:
        """
        指定された主キーに一致する ApplicationFormRoute を更新します。

        Args:
            db_session (Session): DBセッション
            id (int): サロゲートキー
            update_data (dict): 更新内容の辞書

        Returns:
            Optional[ApplicationFormRoute]: 更新後のインスタンスまたは None
        """
        results = self.get_by_key(db_session, id=id)
        instance = results[0] if results else None

        if instance:
            for key, value in update_data.items():
                setattr(instance, key, value)
            db_session.add(instance)

        db_session.flush()
        return instance