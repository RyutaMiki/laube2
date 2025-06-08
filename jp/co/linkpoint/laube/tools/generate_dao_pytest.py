import importlib.util
import inspect
import sys
import os
from pathlib import Path
from jinja2 import Template as JinjaTemplate

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

def to_snake_case(name: str) -> str:
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

model_classes = [
    (name, cls) for name, cls in inspect.getmembers(models, inspect.isclass)
    if hasattr(cls, "__table__") and not name.startswith("_")
]

PYTEST_TEMPLATE = '''\
import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import {{ model_class }}
from jp.co.linkpoint.laube.daos.{{ model_lower }}_dao import {{ dao_class_name }}
from datetime import datetime, date, time
{{ enum_imports }}

@pytest.fixture
def {{ model_lower }}_dict():
    return {
        {%- for col in columns %}
        "{{ col.name }}": {{ col.example }}{% if not loop.last %},{% endif %}
        {%- endfor %}
    }

def test_create_and_get_{{ model_lower }}(db_session: Session, {{ model_lower }}_dict):
    dao = {{ dao_class_name }}()
    obj = dao.create(db_session, {{ model_lower }}_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_{{ model_lower }}(db_session: Session, {{ model_lower }}_dict):
    dao = {{ dao_class_name }}()
    obj = dao.create(db_session, {{ model_lower }}_dict)
    dao.update(db_session, {{ pk_args }}, {"{{ update_col }}": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.{{ update_col }} == "updated"

def test_delete_{{ model_lower }}(db_session: Session, {{ model_lower }}_dict):
    dao = {{ dao_class_name }}()
    obj = dao.create(db_session, {{ model_lower }}_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None
'''

output_dir = PROJECT_DIR / "tests" / "dao"
output_dir.mkdir(parents=True, exist_ok=True)
print("テスト出力先:", output_dir)

for f in output_dir.glob("test_*_dao.py"):
    try:
        f.unlink()
        print(f"[削除] {f}")
    except Exception as e:
        print(f"[削除失敗] {f} ({e})")

from datetime import datetime, date, time

def example_value(col):
    typename = str(col.type).lower()
    if "date" in typename and "time" not in typename:
        return "date(2024, 1, 1)"
    if "timestamp" in typename or "datetime" in typename or "time" in typename:
        return "datetime(2024, 1, 1, 0, 0, 0)"
    if hasattr(col.type, "enum_class"):
        enum_cls = col.type.enum_class
        first_member = list(enum_cls.__members__.keys())[0]
        return f"{enum_cls.__name__}.{first_member}"
    if col.primary_key:
        return 1
    if "char" in typename or "text" in typename or "string" in typename:
        return "'dummy'"
    if "int" in typename:
        return 1
    if "float" in typename or "decimal" in typename:
        return 1.0
    if "bool" in typename:
        return "True"
    return "'dummy'"

for name, model_cls in model_classes:
    columns = []
    for col in model_cls.__table__.columns:
        cname = col.name
        cexample = example_value(col)
        if not cname or not cexample:
            continue
        columns.append({"name": cname, "example": cexample})
    if not columns:
        continue

    model_lower = to_snake_case(name)
    dao_class_name = f"{name}Dao"
    update_col = columns[1]['name'] if len(columns) > 1 else columns[0]['name']

    used_enums = set()
    for col in model_cls.__table__.columns:
        if hasattr(col.type, 'enum_class'):
            used_enums.add(col.type.enum_class.__name__)

    enum_imports = ''
    if used_enums:
        enums_csv = ', '.join(sorted(used_enums))
        enum_imports = f'from jp.co.linkpoint.laube.daos.base.specifiedValue import {enums_csv}'

    pk_fields = [col for col in model_cls.__table__.primary_key.columns]
    pk_args = ", ".join([f"obj.{col.name}" for col in pk_fields])

    template = JinjaTemplate(PYTEST_TEMPLATE)
    rendered = template.render(
        model_class=name,
        model_lower=model_lower,
        dao_class_name=dao_class_name,
        columns=columns,
        update_col=update_col,
        pk_args=pk_args,
        enum_imports=enum_imports,
    )

    test_path = output_dir / f"test_{model_lower}_dao.py"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"[pytest自動生成] {test_path}")

print("pytest用テストコード自動生成 完了！")
