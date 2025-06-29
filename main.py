from fastapi import FastAPI
from app.api.routers import (
    auth_router,
    protected_router,
    common_router,
    access_control_router
)

# アプリケーションインスタンスを生成
app = FastAPI(
    title="Laube2 Engine API",
    description="Laube2 ワークフローエンジン用のAPI群。認証、セキュリティ、業務処理などを含む。",
    version="1.0.0"
)

# 認証系ルート（ログイン、トークン取得など）
app.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["Auth"]
)

# 認証後のみアクセス可能な保護ルート（ユーザー情報取得など）
app.include_router(
    protected_router.router,
    prefix="/secure",
    tags=["Secure"]
)

# 公開・認証済みAPIのサンプル
app.include_router(
    common_router.router,
    prefix="/laube2",
    tags=["Laube2"]
)

# Cerberus Access Control API
app.include_router(
    access_control_router.router,
    prefix="/access-control",
    tags=["Access Control"]
)
