from fastapi import FastAPI
from app.routers import auth, protected
from app.api.laube2_router import router as laube2_router
from app.api import secure_router

# アプリケーションインスタンスを生成
app = FastAPI(
    title="Laube2 Engine API",
    description="Laube2 ワークフローエンジン用のAPI群。認証、セキュリティ、業務処理などを含む。",
    version="1.0.0"
)

# 各ルーターをアプリに登録（登録順も重要）
# 最初にマッチするものが使われるので、プレフィックスの重複には注意

# 認証系ルート（ログイン、トークン取得など）
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

# 認証後のみアクセス可能な保護ルート（ユーザー情報取得など）
app.include_router(
    protected.router,
    prefix="/secure",
    tags=["Secure"]
)

# 業務用Laube2エンジンの実行・制御ルート
app.include_router(
    laube2_router,
    prefix="/laube2",
    tags=["Laube2"]
)

# 簡易トークン認証（Bearer）の例
app.include_router(
    secure_router.router,
    prefix="/secure",
    tags=["Secure Example"]
)
