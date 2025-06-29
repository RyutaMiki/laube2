from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get(
    "/protected",
    summary="認証済みエンドポイント",
    description="認証済みユーザーのみがアクセスできる保護されたルートです。"
)
def read_protected(user: str = Depends(get_current_user)):
    """
    認証が必要な保護ルート。

    このエンドポイントは `Authorization: Bearer <トークン>` を付与してアクセスする必要があります。
    トークンが有効でない場合、401 Unauthorized が返されます。

    Args:
        user (str): `get_current_user` によって取得されたユーザー識別子（通常はユーザーIDやユーザー名）

    Returns:
        dict: 挨拶メッセージを含むJSONレスポンス。
    """
    return {"message": f"Hello {user}, this is a protected route!"}
