import os
import re
from jinja2 import Environment, FileSystemLoader
from inflection import underscore

# パス設定
TEMPLATE_NAME = "generate_stub_service_template.j2"
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../templates"))
REPOSITORY_DIR = os.path.abspath(os.path.join(BASE_DIR, "../repositories"))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../services"))

# クラス名をファイルから抽出する（class XxxRepository）
def extract_repository_classes(filepath):
    classes = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"class\s+(\w+Repository)\b", line)
            if match:
                classes.append(match.group(1))
    return classes

# Serviceスタブを出力
def render_stub_service(repo_class_name: str):
    model_name = repo_class_name.replace("Repository", "")
    model_lower = underscore(model_name)
    dao_file = model_lower + "_repository"
    dao_class_name = repo_class_name
    service_class_name = model_name + "Service"

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template(TEMPLATE_NAME)

    rendered = template.render(
        model_class=model_name,
        dao_class_name=dao_class_name,
        dao_file=dao_file,
        service_class_name=service_class_name
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{model_lower}_service.py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"✅ Generated stub service: {output_path}")

if __name__ == "__main__":
    print(f"📁 TEMPLATE_DIR:     {TEMPLATE_DIR}")
    print(f"📁 REPOSITORY_DIR:   {REPOSITORY_DIR}")
    print(f"📁 OUTPUT_DIR:       {OUTPUT_DIR}\n")

    for filename in os.listdir(REPOSITORY_DIR):
        if filename.endswith("_repository.py"):
            filepath = os.path.join(REPOSITORY_DIR, filename)
            repo_classes = extract_repository_classes(filepath)
            for repo_class in repo_classes:
                render_stub_service(repo_class)
