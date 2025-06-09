import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from contextlib import contextmanager

# .envファイルを読み込み、環境変数に設定する
load_dotenv()

# 使用するデータベースエンジンを環境変数から取得
db_engine = os.getenv("DB_ENGINE", "sqlite")

# データベースURLを構築（PostgreSQL or SQLite）
if db_engine == "postgres":
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif db_engine == "sqlite":
    SQLITE_PATH = os.getenv("SQLITE_PATH", "./laube2.sqlite3")
    DATABASE_URL = f"sqlite:///{SQLITE_PATH}"
else:
    raise ValueError(f"Unknown DB_ENGINE: {db_engine}")

# SQLAlchemyのエンジンを作成する
engine = create_engine(
    DATABASE_URL,
    echo=False,          # Trueにすると実行されたSQLが出力される
    future=True,         # SQLAlchemy 2.0互換モードを有効にする
    pool_pre_ping=True,  # 接続確認を行い、切れた接続を自動で再接続
)

# セッションファクトリを作成（FastAPI依存注入やORM操作で使用）
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

def get_db():
    """
    データベースセッションを生成・クローズするための依存関数。

    FastAPI のエンドポイントで `Depends(get_db)` として使用することで、
    自動的にセッションを生成し、レスポンス後にクローズされる。

    Yields:
        Session: SQLAlchemy ORM セッションインスタンス
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
