from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal  # ※ 適宜インポート先は合わせてね
import logging

logger = logging.getLogger(__name__)

class BaseService:
    """
    サービス共通基底クラス：セッション管理（生成・クローズ・トランザクション）を一括管理
    """

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        セッションの生成とクローズを管理するコンテキストマネージャ
        """
        db: Session = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def transaction(self) -> Generator[Session, None, None]:
        """
        トランザクション付きセッションを提供（commit/rollbackを自動管理）
        """
        with self.get_session() as db:
            try:
                yield db
                db.commit()
            except Exception as e:
                db.rollback()
                logger.exception("トランザクションでエラーが発生しました")
                raise
