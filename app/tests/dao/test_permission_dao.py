import pytest
from sqlalchemy.orm import Session
from app.models.models import Permission
from app.daos.permission_dao import PermissionDao
from datetime import datetime, date, time


@pytest.fixture
def permission_dict():
    return {
        "id": 1,
        "permission_id": 'dummy',
        "permission_name": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_permission(db_session: Session, permission_dict):
    dao = PermissionDao()
    obj = dao.create(db_session, permission_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_permission(db_session: Session, permission_dict):
    dao = PermissionDao()
    obj = dao.create(db_session, permission_dict)
    dao.update(db_session, obj.id, {"permission_id": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.permission_id == "updated"

def test_delete_permission(db_session: Session, permission_dict):
    dao = PermissionDao()
    obj = dao.create(db_session, permission_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None