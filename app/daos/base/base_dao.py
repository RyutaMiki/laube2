from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class BaseDao(Generic[T]):
    """
    共通DAO基底クラス

    サブクラスで `model` 属性を必ずセットしてください。
    """

    model = None  # 継承先で必ずセットする

    def get_by_key(self, db_session: Session, id: int) -> List[T]:
        """
        主キー（id）でレコードを取得します。

        Args:
            db_session (Session): SQLAlchemyのDBセッション
            id (int): 取得したいレコードのID

        Returns:
            List[T]: 該当レコード（なければ空リスト）
        """
        query = db_session.query(self.model)
        if id is not None:
            query = query.filter(self.model.id == id)
        return query.all()

    def insert(self, db_session: Session, instance: T) -> T:
        """
        新規レコードを追加します。

        Args:
            db_session (Session): SQLAlchemyのDBセッション
            instance (T): 追加したいモデルインスタンス

        Returns:
            T: 追加されたインスタンス
        """
        db_session.add(instance)
        db_session.flush()
        return instance

    def delete(self, db_session: Session, instance: T) -> None:
        """
        指定したレコードを削除します。

        Args:
            db_session (Session): SQLAlchemyのDBセッション
            instance (T): 削除したいモデルインスタンス

        Returns:
            None
        """
        db_session.delete(instance)
        db_session.flush()

    def get_all(self, db_session: Session, limit: int = 100, offset: int = 0) -> List[T]:
        """
        全レコードを取得します（ページング対応）。

        Args:
            db_session (Session): SQLAlchemyのDBセッション
            limit (int, optional): 取得件数の上限（デフォルト100）
            offset (int, optional): 取得開始位置（デフォルト0）

        Returns:
            List[T]: レコードリスト
        """
        return db_session.query(self.model).limit(limit).offset(offset).all()

    def count(self, db_session: Session) -> int:
        """
        レコードの総数をカウントします。

        Args:
            db_session (Session): SQLAlchemyのDBセッション

        Returns:
            int: レコード総数
        """
        return db_session.query(func.count()).select_from(self.model).scalar()

    def update(self, db_session: Session, id: int, update_data: dict) -> Optional[T]:
        """
        指定したIDのレコードを更新します。

        Args:
            db_session (Session): SQLAlchemyのDBセッション
            id (int): 更新対象レコードのID
            update_data (dict): 更新内容（カラム名: 値）

        Returns:
            Optional[T]: 更新後のインスタンス（なければNone）
        """
        results = self.get_by_key(db_session, id=id)
        instance = results[0] if results else None
        if instance:
            for key, value in update_data.items():
                setattr(instance, key, value)
            db_session.add(instance)
        db_session.flush()
        return instance
