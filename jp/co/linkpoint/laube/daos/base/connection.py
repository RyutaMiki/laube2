import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env読込
load_dotenv()

db_engine = os.getenv("DB_ENGINE", "sqlite")

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

# エンジン生成
engine = create_engine(
    DATABASE_URL,
    echo=False,  # SQLログ出したいならTrue
    future=True,  # SQLAlchemy 1.4以降推奨
    pool_pre_ping=True,  # コネクション自動再接続
)

# セッション生成
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# 使い方例
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
