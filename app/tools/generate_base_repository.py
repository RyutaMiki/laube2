import os
import importlib
import inspect
import re
from jinja2 import Environment, FileSystemLoader
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

DAO_DIRS = [
    "app/daos",
    "app/daos/base"
]
REPO_BASE_DIR = "app/repositories/base"
REPO_DIR = "app/repositories"
TEMPLATE_DIR = "app/templates"
MODEL_IMPORT_PATH = "app.models.models"
MODEL_MAP = {}

SKIP_DAO_FILES = {"base_dao.py"}

def snake_to_camel(name):
    return ''.join(word.title() for word in name.replace('.py', '').split('_'))

def camel_to_snake(name):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def scan_dao_files():
    dao_files = []
    for dao_dir in DAO_DIRS:
        for root, dirs, files in os.walk(dao_dir):
            for file in files:
                # base_dao.py だけは完全スキップ
                if file in SKIP_DAO_FILES:
                    continue
                # _dao.py や _dao_base.py のみ対象
                if file.endswith("_dao.py") or file.endswith("_dao_base.py"):
                    dao_files.append((root, file))
    return dao_files

def get_public_methods(clazz):
    return [
        {
            "name": name,
            "args": [
                arg for arg in inspect.signature(method).parameters.keys() if arg != "self"
            ],
        }
        for name, method in inspect.getmembers(clazz, predicate=inspect.isfunction)
        if not name.startswith("_")
    ]

def render_template(template_name, params):
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_name)
    return template.render(**params)

def generate_base_repository_for_dao(dao_module_path, dao_class_name, model_import_path, model_class_name, output_file):
    dao_module = importlib.import_module(dao_module_path)
    dao_class = getattr(dao_module, dao_class_name)
    dao_methods = get_public_methods(dao_class)

    # ★ここで正規化して「BaseBase」にならないように！
    repository_base_class_name = dao_class_name.replace("DaoBase", "RepositoryBase").replace("Dao", "RepositoryBase")
    repository_base_class_name = repository_base_class_name.replace("BaseBase", "Base")

    repository_base_file_name = camel_to_snake(repository_base_class_name)
    params = {
        "dao_import_path": dao_module_path,
        "dao_class_name": dao_class_name,
        "model_import_path": model_import_path,
        "model_class_name": model_class_name,
        "repository_base_class_name": repository_base_class_name,
        "repository_base_file_name": repository_base_file_name,
        "dao_methods": dao_methods,
    }
    content = render_template("generate_base_repository_template.j2", params)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] BaseRepository生成: {output_file}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] BaseRepository生成: {output_file}")

def generate_stub_repository(dao_class_name, output_file):
    repository_base_class_name = f"{dao_class_name.replace('Dao', 'RepositoryBase')}"
    repository_base_file_name = camel_to_snake(repository_base_class_name)
    repository_class_name = f"{dao_class_name.replace('Dao', 'Repository')}"
    params = {
        "repository_base_class_name": repository_base_class_name,
        "repository_base_file_name": repository_base_file_name,
        "repository_class_name": repository_class_name,
    }
    content = render_template("generate_stub_repository_template.j2", params)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Repository stub生成: {output_file}")

def main():
    os.makedirs(REPO_BASE_DIR, exist_ok=True)
    os.makedirs(REPO_DIR, exist_ok=True)

    for root, file in scan_dao_files():
        # モジュールパス生成
        module_rel_path = os.path.relpath(os.path.join(root, file), '.').replace(os.sep, '.')[:-3]
        dao_module_path = module_rel_path
        dao_class_name = snake_to_camel(file.replace(".py", ""))

        # "base"ディレクトリ直下のbase_dao_base.pyでもBase始まりは除外
        if dao_class_name.startswith("Base") and file == "base_dao_base.py":
            continue

        model_class_name = MODEL_MAP.get(dao_class_name, dao_class_name.replace("Dao", "").replace("Base", ""))

        # 1. baseリポジトリのみ生成
        base_file_name = camel_to_snake(dao_class_name.replace("DaoBase", "RepositoryBase").replace("Dao", "RepositoryBase")) + ".py"
        output_base_file = os.path.join(REPO_BASE_DIR, base_file_name)
        try:
            generate_base_repository_for_dao(
                dao_module_path=dao_module_path,
                dao_class_name=dao_class_name,
                model_import_path=MODEL_IMPORT_PATH,
                model_class_name=model_class_name,
                output_file=output_base_file
            )
        except Exception as e:
            print(f"[NG] {dao_class_name} Base生成失敗: {e}")

        # 2. stubリポジトリは「実体daoのみ」でOK（base_dao_base.py, base_dao.pyからは生成しない）

        # 実体DAOだけstubも生成したい場合はここで判定追加
        if file.endswith("_dao.py") and not root.endswith("/base"):
            stub_file_name = camel_to_snake(dao_class_name.replace("Dao", "Repository")) + ".py"
            output_stub_file = os.path.join(REPO_DIR, stub_file_name)
            if not os.path.exists(output_stub_file):
                try:
                    generate_stub_repository(dao_class_name, output_stub_file)
                except Exception as e:
                    print(f"[NG] {dao_class_name} stub生成失敗: {e}")
            else:
                print(f"[SKIP] {output_stub_file} は既に存在するのでスキップ")

if __name__ == "__main__":
    main()
