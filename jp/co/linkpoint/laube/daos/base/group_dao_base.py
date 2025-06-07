from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.base_dao import BaseDao
from jp.co.linkpoint.laube.daos.base.models import Group

from datetime import datetime, date


class BaseGroupDao(BaseDao[Group]):
    """
    Data Access Object for Group.
    """
    model = Group

    def get_by_key(self, db_session: Session, id: int) -> List[Group]:
        """
        Group を指定された主キー条件であいまい取得します。

        Args:
            db_session (Session): DBセッション
            id (Optional[int]): サロゲートキー（指定された場合のみ条件に含めます）

        Returns:
            List[Group]: 条件に一致するレコードのリスト
        """
        query = db_session.query(Group)
        if id is not None:
            query = query.filter(Group.id == id)
        return query.all()

    def insert(self, db_session: Session, instance: Group) -> Group:
        """
        Group を登録します。

        Args:
            db_session (Session): DBセッション
            instance (Group): 保存するインスタンス

        Returns:
            Group: 保存後のインスタンス
        """
        db_session.add(instance)
        db_session.flush()
        return instance

    def delete(self, db_session: Session, instance: Group) -> None:
        """
        Group を削除します。

        Args:
            db_session (Session): DBセッション
            instance (Group): 削除するインスタンス

        Returns:
            None
        """
        db_session.delete(instance)
        db_session.flush()

    def get_all(self, db_session: Session, limit: int = 100, offset: int = 0) -> List[Group]:
        """
        Group を全件取得します（ページング対応）。

        Args:
            db_session (Session): DBセッション
            limit (int): 最大取得件数
            offset (int): 取得開始位置

        Returns:
            List[Group]: 取得されたインスタンスのリスト
        """
        return db_session.query(Group).limit(limit).offset(offset).all()

    def count(self, db_session: Session) -> int:
        """
        Group の総件数を取得します。

        Args:
            db_session (Session): DBセッション

        Returns:
            int: 件数
        """
        return db_session.query(func.count()).select_from(Group).scalar()

    def update(self, db_session: Session, id: int, update_data: dict) -> Optional[Group]:
        """
        指定された主キーに一致する Group を更新します。

        Args:
            db_session (Session): DBセッション
            id (int): サロゲートキー
            update_data (dict): 更新内容の辞書

        Returns:
            Optional[Group]: 更新後のインスタンスまたは None
        """
        results = self.get_by_key(db_session, id=id)
        instance = results[0] if results else None

        if instance:
            for key, value in update_data.items():
                setattr(instance, key, value)
            db_session.add(instance)

        db_session.flush()
        return instance