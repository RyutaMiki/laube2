import importlib.util
import inspect
import sys
import os
from pathlib import Path

# === パス・env設定 ===
sys.path.insert(0, os.getenv("PROJECT_DIR") or "d:/git/laube2")
from dotenv import load_dotenv
load_dotenv()
PROJECT_DIR = Path(os.getenv("PROJECT_DIR") or "d:/git/laube2")
MODELS_FILE = PROJECT_DIR / "jp" / "co" / "linkpoint" / "laube" / "daos" / "base" / "models.py"

# models.pyをimport
spec = importlib.util.spec_from_file_location("models", MODELS_FILE)
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)

# === モデル一覧取得 ===
def to_snake_case(name: str) -> str:
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

model_classes = [
    (name, cls) for name, cls in inspect.getmembers(models, inspect.isclass)
    if hasattr(cls, "__table__") and not name.startswith("_")
]

# === テストテンプレート ===
PYTEST_TEMPLATE = '''\
import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import {{ model_class }}
from jp.co.linkpoint.laube.daos.{{ model_lower }}_dao import {{ dao_class_name }}

@pytest.fixture
def {{ model_lower }}_dict():
    return {
        {% for col in columns -%}
        "{{ col.name }}": {{ col.example }},
        {% endfor %}
    }

def test_create_and_get_{{ model_lower }}(db_session: Session, {{ model_lower }}_dict):
    dao = {{ dao_class_name }}()
    obj = dao.create(db_session, {{ model_lower }}_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_{{ model_lower }}(db_session: Session, {{ model_lower }}_dict):
    dao = {{ dao_class_name }}()
    obj = dao.create(db_session, {{ model_lower }}_dict)
    dao.update(db_session, obj.id, {"{{ update_col }}": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.{{ update_col }} == "updated"

def test_delete_{{ model_lower }}(db_session: Session, {{ model_lower }}_dict):
    dao = {{ dao_class_name }}()
    obj = dao.create(db_session, {{ model_lower }}_dict)
    dao.delete(db_session, obj.id)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None
'''

# === テストファイル出力先 ===
output_dir = PROJECT_DIR / "tests" / "dao"
output_dir.mkdir(parents=True, exist_ok=True)
print("テスト出力先:", output_dir)

# === 既存のテストファイルを全削除 ===
for f in output_dir.glob("test_*_dao.py"):
    try:
        f.unlink()
        print(f"[削除] {f}")
    except Exception as e:
        print(f"[削除失敗] {f} ({e})")

# === 型ごとのサンプル値 ===
def example_value(col):
    import datetime
    if col.primary_key:
        return 1
    typename = str(col.type).lower()
    if "char" in typename or "text" in typename or "string" in typename:
        return "'dummy'"
    if "int" in typename:
        return 1
    if "float" in typename or "decimal" in typename:
        return 1.0
    if "bool" in typename:
        return "True"
    if "date" in typename and "time" not in typename:
        return "'2024-01-01'"
    if "time" in typename or "timestamp" in typename:
        return "'2024-01-01T00:00:00'"
    # EnumTypeや特殊型
    return "'dummy'"

# === テンプレートエンジン（Jinja2でシンプルに） ===
from jinja2 import Template as JinjaTemplate

for name, model_cls in model_classes:
    columns = []
    for col in model_cls.__table__.columns:
        columns.append({
            "name": col.name,
            "example": example_value(col)
        })
    if not columns:
        continue

    model_lower = to_snake_case(name)
    dao_class_name = f"{name}Dao"
    update_col = columns[1]['name'] if len(columns) > 1 else columns[0]['name']

    # テンプレート埋め込み
    template = JinjaTemplate(PYTEST_TEMPLATE)
    rendered = template.render(
        model_class=name,
        model_lower=model_lower,
        dao_class_name=dao_class_name,
        columns=columns,
        update_col=update_col,
    )

    # ファイル出力
    test_path = output_dir / f"test_{model_lower}_dao.py"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"[pytest自動生成] {test_path}")

print("pytest用テストコード自動生成 完了！")
