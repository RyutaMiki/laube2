# routers/common_router.py
from fastapi import APIRouter, Depends
from app.dependencies.auth import verify_token

router = APIRouter()


@router.get("/health")
def public_endpoint():
    return {"message": "誰でも参照可能"}

@router.get("/secure-data", dependencies=[Depends(verify_token)])
def protected_endpoint():
    return {"message": "認証通過"}
