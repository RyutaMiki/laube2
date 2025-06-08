import sys
import os
import re
import importlib.util
import inspect
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from dotenv import load_dotenv
load_dotenv()

# ====== パス定義 ======
PROJECT_DIR = Path(os.getenv("PROJECT_DIR") or Path(__file__).resolve().parents[1])  # laube2/app/想定
APP_DIR = PROJECT_DIR  # laube2/app/

MODELS_FILE = APP_DIR / "models" / "models.py"
TEMPLATE_DIR = APP_DIR / "templates"
DAO_DIR = APP_DIR / "daos"
DAO_BASE_DIR = DAO_DIR / "base"

# パス追加（import用）
sys.path.insert(0, str(APP_DIR))

DAO_DIR.mkdir(parents=True, exist_ok=True)
DAO_BASE_DIR.mkdir(parents=True, exist_ok=True)

# === Base DAO全削除（自動生成分だけ消す。他は絶対消さない！） ===
for file in DAO_BASE_DIR.glob("*_dao_base.py"):
    try:
        file.unlink()
        print(f"[Base DAO削除] {file}")
    except Exception as e:
        print(f"[Base DAO削除失敗] {file}: {e}")

# === Jinja2環境構築 ===
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), trim_blocks=True, lstrip_blocks=True)
dao_base_template = env.get_template("generate_base_dao_template.j2")
dao_stub_template = env.get_template("generate_stub_dao_template.j2")

# === models.py 読み込み ===
spec = importlib.util.spec_from_file_location("models", MODELS_FILE)
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)

# === ヘルパー関数 ===
def to_snake_case(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def get_column_type(col):
    try:
        return col.type.python_type.__name__
    except Exception:
        return "str"  # fallback

def get_pk_fields_with_comments(model_cls):
    pk_fields = []
    for col in model_cls.__table__.primary_key.columns:
        comment = col.comment or col.name
        comment = re.sub(r"（必須）|（任意）", "", comment).strip()
        pk_fields.append({
            "name": col.name,
            "type": get_column_type(col),
            "comment": comment
        })
    return pk_fields

# === モデル一覧取得 ===
model_classes = [
    (name, cls) for name, cls in inspect.getmembers(models, inspect.isclass)
    if hasattr(cls, "__table__") and not name.startswith("_")
]

print(f"[INFO] モデルクラス数: {len(model_classes)}")

# === DAOファイル自動生成 ===
for original_name, model_cls in model_classes:

    used_types = set()
    for col in model_cls.__table__.columns:
        try:
            used_types.add(col.type.python_type.__name__)
        except Exception:
            pass

    model_snake = to_snake_case(original_name)
    model_pascal = original_name

    base_dao_class_name = f"Base{model_pascal}Dao"
    dao_class_name = f"{model_pascal}Dao"

    pk_fields = get_pk_fields_with_comments(model_cls)

    # Base DAO生成（毎回）
    base_path = DAO_BASE_DIR / f"{model_snake}_dao_base.py"
    rendered_base = dao_base_template.render(
        model_class=model_pascal,
        model_lower=model_snake,
        base_dao_class_name=base_dao_class_name,
        pk_fields=pk_fields,
        imports=used_types
    )
    with open(base_path, "w", encoding="utf-8") as f:
        f.write(rendered_base)
    print(f"[Base DAO生成完了] {base_path}")

    # Stub DAO生成（初回のみ）
    stub_path = DAO_DIR / f"{model_snake}_dao.py"
    if not stub_path.exists():
        rendered_stub = dao_stub_template.render(
            model_class=model_pascal,
            model_lower=model_snake,
            base_dao_class_name=base_dao_class_name,
            dao_class_name=dao_class_name
        )
        with open(stub_path, "w", encoding="utf-8") as f:
            f.write(rendered_stub)
        print(f"[Stub DAO初回作成] {stub_path}")
    else:
        print(f"[スキップ] {stub_path} は既に存在（独自コード保持）")

print("[INFO] DAO自動生成 完了！")
