import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from inflection import underscore

# テンプレートファイル名
TEMPLATE_NAME = "generate_base_service_template.j2"

# テンプレートのディレクトリ: app/templates
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates"))

# 出力先ディレクトリ: app/services/base
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../services/base"))


def render_base_service(model_class: str):
    model_lower = underscore(model_class)
    base_dao_class_name = f"{model_class}DaoBase"
    base_service_class_name = f"{model_class}ServiceBase"

    # Jinja2環境設定
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True
    )

    try:
        template = env.get_template(TEMPLATE_NAME)
    except TemplateNotFound:
        print(f"❌ テンプレートが見つかりません: {TEMPLATE_NAME}")
        print(f"🔍 探索ディレクトリ: {TEMPLATE_DIR}")
        return

    rendered = template.render(
        model_class=model_class,
        model_lower=model_lower,
        base_dao_class_name=base_dao_class_name,
        base_service_class_name=base_service_class_name,
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{model_lower}_service_base.py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ Generated: {output_path}")


if __name__ == "__main__":
    # 自動生成対象のモデルクラス名
    model_classes = [
        "User",
        "Project",
        "ActivityObject"
    ]

    print(f"📁 TEMPLATE_DIR: {TEMPLATE_DIR}")
    print(f"📁 OUTPUT_DIR:   {OUTPUT_DIR}\n")

    for model in model_classes:
        render_base_service(model)
