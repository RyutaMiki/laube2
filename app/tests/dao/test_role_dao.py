import pytest
from sqlalchemy.orm import Session
from app.models.models import Role
from app.daos.role_dao import RoleDao
from datetime import datetime, date, time


@pytest.fixture
def role_dict():
    return {
        "id": 1,
        "role_id": 'dummy',
        "role_name": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_role(db_session: Session, role_dict):
    dao = RoleDao()
    obj = dao.create(db_session, role_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_role(db_session: Session, role_dict):
    dao = RoleDao()
    obj = dao.create(db_session, role_dict)
    dao.update(db_session, obj.id, {"role_id": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.role_id == "updated"

def test_delete_role(db_session: Session, role_dict):
    dao = RoleDao()
    obj = dao.create(db_session, role_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None