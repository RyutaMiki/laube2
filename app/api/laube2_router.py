# app/api/laube2_router.py
from fastapi import APIRouter, HTTPException
from app.services.laube2_service import Laube2Service

router = APIRouter()
service = Laube2Service()

@router.get("/health")
def health_check():
    return {"status": service.health_check()}

@router.post("/execute")
def execute_task(payload: dict):
    try:
        result = service.do_something(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
