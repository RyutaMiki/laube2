from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import decode_access_token

# OAuth2のパスワード認証フローに基づくスキーマ
# Swagger UI では /login エンドポイントでトークンを取得することが前提となる
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    アクセストークンをデコードし、認証済みユーザー情報を取得する依存関数。

    FastAPI のルート関数で `Depends(get_current_user)` として使用することで、
    リクエストヘッダーの Bearer トークンを自動的に取得・検証できる。

    Args:
        token (str): リクエストの Authorization ヘッダーから取得された Bearer トークン。

    Returns:
        str: トークンからデコードされたユーザー識別子（通常はユーザーIDやメールアドレスなど）。

    Raises:
        HTTPException: トークンの検証に失敗した場合（例：署名不正、有効期限切れなど）。
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]
