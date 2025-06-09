# app/main.py
from fastapi import FastAPI
from app.api.laube2_router import router as laube2_router

app = FastAPI(title="Laube2 Engine API")

# ルーターを登録
app.include_router(laube2_router, prefix="/laube2", tags=["Laube2"])
