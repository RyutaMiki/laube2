import sys
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql
import sys
import sqlalchemy
print("Python version:", sys.version)
print("SQLAlchemy version:", sqlalchemy.__version__)

# ==== プロジェクトのパスを設定 ====
sys.path.insert(0, os.getenv("PROJECT_DIR") or "d:/git/laube2")

# ==== models.py のパス設定 ====
from dotenv import load_dotenv
load_dotenv()
PROJECT_DIR = Path(os.getenv("PROJECT_DIR") or "d:/git/laube2")
MODELS_FILE = PROJECT_DIR / "jp" / "co" / "linkpoint" / "laube" / "daos" / "base" / "models.py"

# ==== models.py 読み込み ====
import importlib.util

spec = importlib.util.spec_from_file_location("models", MODELS_FILE)
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)

# ==== CREATE TABLE SQL出力処理 ====
def output_create_table_sql(output_path="create_tables.sql"):
    engine = create_engine("sqlite:///:memory:")  # SQLite方言（MySQLなどにしたい場合は後述）
    sql_lines = []
    print("テーブル一覧:", [t.name for t in models.Base.metadata.sorted_tables])


    for table in models.Base.metadata.sorted_tables:
        print(f"\n[DEBUG] {table.name}: columns={list(table.columns.keys())}")
        try:
            # ここでcompileできるか？
            create_sql = str(table.compile(dialect=postgresql.dialect()))
            if not create_sql or create_sql.strip() == "":
                print(f"[空SQL] {table.name} → '{create_sql}'（何も出力されていません）")
            else:
                print(f"[生成成功] {table.name}:\n{create_sql}\n")
            sql_lines.append(f"-- {table.name}\n{create_sql.strip()};")
        except Exception as e:
            print(f"[例外発生] {table.name}: {e}")
            sql_lines.append(f"-- {table.name}\n-- [生成失敗: {e}]")




    output_path = PROJECT_DIR / output_path
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(sql_lines))
    print(f"[CREATE TABLE SQL出力完了] {output_path}")

if __name__ == "__main__":
    output_create_table_sql()
