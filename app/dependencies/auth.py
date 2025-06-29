from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
import logging
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


security = HTTPBearer()


def verify_token(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    BearerトークンによるAPI認証を行う依存関数。

    この関数はFastAPIのDependsとして使用され、Authorizationヘッダーに含まれる
    Bearerトークンを検証する。トークンが不正な場合は403エラーを返し、
    ログにクライアントIPおよび受信トークンを記録する。

    Parameters:
    ----------
    request : Request
        リクエスト情報（クライアントIP取得のために使用）
    credentials : HTTPAuthorizationCredentials
        Authorizationヘッダーに含まれるBearerトークン情報（自動でDependsされる）

    Raises:
    ------
    HTTPException
        トークンが不正な場合に403 Forbiddenを返す

    Usage:
    ------
    @router.get("/secure-endpoint", dependencies=[Depends(verify_token)])
    def secure_route(): ...
    """
    token = credentials.credentials
    if token != "secret-token-123":
        logging.warning(f"認証失敗: IP={request.client.host}, トークン={token}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
