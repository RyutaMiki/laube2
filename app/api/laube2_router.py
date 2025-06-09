from fastapi import APIRouter, HTTPException
from app.services.laube2_service import Laube2Service

router = APIRouter()
service = Laube2Service()

@router.get("/health", summary="ヘルスチェック", description="Laube2エンジンの稼働確認用エンドポイント。")
def health_check():
    """
    Laube2エンジンが正常に稼働しているかを確認します。
    
    Returns:
        dict: サービスの稼働状態を表すステータス。
    """
    return {"status": service.health_check()}

@router.post("/execute", summary="Laube2の処理実行", description="Laube2エンジンに任意のペイロードを渡して処理を実行します。")
def execute_task(payload: dict):
    """
    任意のペイロードを元にLaube2の処理を実行します。

    Args:
        payload (dict): 実行対象の入力データ。

    Returns:
        Any: 実行結果のデータ。

    Raises:
        HTTPException: 実行中に例外が発生した場合、500エラーを返します。
    """
    try:
        result = service.do_something(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
