# main.py
from fastapi import FastAPI
from app.api.routers import access_control_router, common_router  # あなたの構成に合わせて調整！

app = FastAPI(
    title="Cerberus Access Control API",
    description="権限・ロール・リソース制御のためのAPI",
    version="1.0.0"
)

# ルーターを登録
app.include_router(common_router.router)
app.include_router(access_control_router.router)

# ルートにもヘルスチェックを追加（任意）
@app.get("/")
def read_root():
    return {"message": "FastAPI is alive!"}
