# routers/access_control_router.py
from fastapi import APIRouter, Depends
from app.engine.cerberus import Cerberus
from app.dependencies.auth import verify_token

router = APIRouter(prefix="/access-control", tags=["Access Control"])
engine = Cerberus()

# 保護された操作群
@router.post("/user/{user_id}/role/{role_id}", dependencies=[Depends(verify_token)])
def assign_role(user_id: str, role_id: str):
    return engine.assign_role_to_user(user_id, role_id)

@router.delete("/user/{user_id}/role/{role_id}", dependencies=[Depends(verify_token)])
def revoke_role(user_id: str, role_id: str):
    engine.revoke_role_from_user(user_id, role_id)
    return {"detail": "Role removed"}

@router.post("/role/{role_id}/permission/{permission_id}", dependencies=[Depends(verify_token)])
def assign_permission(role_id: str, permission_id: str):
    return engine.assign_permission_to_role(role_id, permission_id)

@router.delete("/role/{role_id}/permission/{permission_id}", dependencies=[Depends(verify_token)])
def revoke_permission(role_id: str, permission_id: str):
    engine.revoke_permission_from_role(role_id, permission_id)
    return {"detail": "Permission removed"}

@router.post("/policy", dependencies=[Depends(verify_token)])
def assign_resource(role_id: str, permission_id: str, resource_id: str, condition: str = None):
    return engine.assign_resource_to_role(role_id, permission_id, resource_id, condition)

@router.delete("/policy", dependencies=[Depends(verify_token)])
def revoke_resource(role_id: str, permission_id: str, resource_id: str):
    engine.revoke_resource_from_role(role_id, permission_id, resource_id)
    return {"detail": "Policy removed"}
