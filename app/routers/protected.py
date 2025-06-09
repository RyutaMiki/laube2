from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/protected")
def read_protected(user: str = Depends(get_current_user)):
    return {"message": f"Hello {user}, this is a protected route!"}