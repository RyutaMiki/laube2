from fastapi import FastAPI
from app.routers import auth, protected
from app.api.laube2_router import router as laube2_router

app = FastAPI(title="Laube2 Engine API")

# ルーターを登録（順番も意味あるよ！）
app.include_router(auth.router, prefix="/auth", tags=["Auth"])           # 認証系（ログインなど）
app.include_router(protected.router, prefix="/secure", tags=["Secure"])  # 認証が必要なAPI
app.include_router(laube2_router, prefix="/laube2", tags=["Laube2"])     # 業務用エンジン
