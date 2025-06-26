import pytest
from sqlalchemy.orm import Session
from app.models.models import UserRole
from app.daos.user_role_dao import UserRoleDao
from datetime import datetime, date, time


@pytest.fixture
def user_role_dict():
    return {
        "id": 1,
        "user_id": 'dummy',
        "role_id": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_user_role(db_session: Session, user_role_dict):
    dao = UserRoleDao()
    obj = dao.create(db_session, user_role_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_user_role(db_session: Session, user_role_dict):
    dao = UserRoleDao()
    obj = dao.create(db_session, user_role_dict)
    dao.update(db_session, obj.id, {"user_id": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.user_id == "updated"

def test_delete_user_role(db_session: Session, user_role_dict):
    dao = UserRoleDao()
    obj = dao.create(db_session, user_role_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None