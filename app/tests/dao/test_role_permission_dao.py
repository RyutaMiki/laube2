import pytest
from sqlalchemy.orm import Session
from app.models.models import RolePermission
from app.daos.role_permission_dao import RolePermissionDao
from datetime import datetime, date, time


@pytest.fixture
def role_permission_dict():
    return {
        "id": 1,
        "role_id": 'dummy',
        "permission_id": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_role_permission(db_session: Session, role_permission_dict):
    dao = RolePermissionDao()
    obj = dao.create(db_session, role_permission_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_role_permission(db_session: Session, role_permission_dict):
    dao = RolePermissionDao()
    obj = dao.create(db_session, role_permission_dict)
    dao.update(db_session, obj.id, {"role_id": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.role_id == "updated"

def test_delete_role_permission(db_session: Session, role_permission_dict):
    dao = RolePermissionDao()
    obj = dao.create(db_session, role_permission_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None