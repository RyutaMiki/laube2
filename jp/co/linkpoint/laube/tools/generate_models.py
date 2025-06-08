#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generate_models.py - 完全版
"""

import sys
import json
import re
import traceback
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# ------------------------------------------------------------
# 1. 入力ファイルを決定
# ------------------------------------------------------------
if len(sys.argv) >= 2:
    src_file = Path(sys.argv[1])
else:
    src_file = Path("schema.yaml")
    print(f"[INFO] 引数が無いので {src_file} を読みます")

if not src_file.exists():
    sys.exit(f"[ERROR] ファイルが見つかりません: {src_file.resolve()}")

# ------------------------------------------------------------
# 2. JSON / YAML ロード
# ------------------------------------------------------------
def load_file(path: Path):
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("[ERROR] PyYAML が未インストールです → pip install pyyaml")
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    return json.loads(path.read_text(encoding="utf-8"))

try:
    data = load_file(src_file)
except Exception as e:
    traceback.print_exc()
    sys.exit(f"[ERROR] ファイル読込エラー: {e}")

if isinstance(data, list):
    models_list = data
elif isinstance(data, dict) and isinstance(data.get("models"), list):
    models_list = data["models"]
else:
    sys.exit("[ERROR] ルートが list でも dict(models=[]) でもありません。")

print(f"[DEBUG] 読み込んだモデル数: {len(models_list)}")

# ------------------------------------------------------------
# 3. Jinja2 環境
# ------------------------------------------------------------
# テンプレートディレクトリは「tools」の1つ上の「templates」 or 「template」等にしておく
TEMPLATE_CANDIDATES = [
    Path(__file__).parent.parent / "templates",   # 普通ここ
    Path(__file__).parent.parent / "template",    # たまに"s"無しパターンも
    Path(__file__).parent / "templates",
    Path(__file__).parent / "template"
]

TEMPLATE_NAME = "models_template.j2"
TEMPLATE_DIR = None

for candidate in TEMPLATE_CANDIDATES:
    if (candidate / TEMPLATE_NAME).exists():
        TEMPLATE_DIR = candidate
        break

if not TEMPLATE_DIR:
    print("[ERROR] テンプレートが見つかりません。以下のパスをチェックして！")
    for candidate in TEMPLATE_CANDIDATES:
        print("  -", candidate.resolve())
    sys.exit(f"[ERROR] テンプレート '{TEMPLATE_NAME}' が見つからない！")

print(f"[DEBUG] TEMPLATE_DIR: {TEMPLATE_DIR.resolve()}")
print(f"[DEBUG] テンプレート一覧: {[f.name for f in TEMPLATE_DIR.glob('*')]}")

env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape([]),
    trim_blocks=True,
    lstrip_blocks=True,
)
env.filters["regex_replace"] = lambda v, p, r: re.sub(p, r, v)

# テンプレ取得
try:
    template = env.get_template(TEMPLATE_NAME)
except Exception as e:
    traceback.print_exc()
    sys.exit(f"[ERROR] テンプレート読み込み失敗: {TEMPLATE_NAME} : {e}")

# ------------------------------------------------------------
# 4. レンダリング
# ------------------------------------------------------------
try:
    rendered = template.render(models=models_list)
except Exception:
    traceback.print_exc()
    sys.exit("[ERROR] テンプレートレンダリングで例外発生 → 上のトレースを確認")

# ------------------------------------------------------------
# 5. 出力
# ------------------------------------------------------------
# 出力先: jp/co/linkpoint/laube/daos/base/models.py
BASE_DAO_DIR = Path(__file__).parent.parent / "daos" / "base"
BASE_DAO_DIR.mkdir(parents=True, exist_ok=True)

output_file = BASE_DAO_DIR / "models.py"
if output_file.exists():
    output_file.unlink()   # ← ここを追加

try:
    output_file.write_text(rendered, encoding="utf-8")
    print(f"生成完了: {output_file.resolve()}")
except Exception as e:
    traceback.print_exc()
    sys.exit(f"[ERROR] 書き込み失敗: {e}")