from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import User
from app.database.connection import get_db
from app.utils.security import verify_password
from app.utils.jwt import create_access_token
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    """
    ログインリクエストのデータモデル。

    Attributes:
        username (str): ユーザー名
        password (str): パスワード（平文）
    """
    username: str
    password: str

@router.post(
    "/login",
    summary="ユーザーログイン",
    description="ユーザー名とパスワードを検証し、認証トークン（JWT）を発行します。"
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    ログイン処理エンドポイント。

    ユーザー名とパスワードを受け取り、認証に成功した場合はアクセストークンを返します。
    トークンは後続のAPI呼び出しで `Authorization: Bearer <token>` として使用します。

    Args:
        data (LoginRequest): ユーザー名とパスワードを含むリクエストボディ。
        db (Session): データベースセッション。FastAPIによって自動注入されます。

    Returns:
        dict: `access_token`（JWT）と `token_type`（常に "bearer"）を含む辞書。

    Raises:
        HTTPException: 認証失敗時に 401 Unauthorized を返します。
    """
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
