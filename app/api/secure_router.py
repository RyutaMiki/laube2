from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Bearerトークンの検証を行う。
    トークンが 'secret-token-123' でない場合は403を返す。
    """
    token = credentials.credentials
    if token != "secret-token-123":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )

@router.get("/health", summary="ヘルスチェック", description="認証不要の公開エンドポイント。")
def public_endpoint():
    """
    サーバーの状態を確認するための公開エンドポイント。
    """
    return {"message": "誰でも見れる"}

@router.get("/secure-data", summary="機密データ取得", description="認証トークンが必要なエンドポイント。", dependencies=[Depends(verify_token)])
def protected_endpoint():
    """
    Bearer認証を通過したユーザーにだけ返す秘密のデータ。
    """
    return {"message": "お、認証されたね。これが秘密のデータだ"}
