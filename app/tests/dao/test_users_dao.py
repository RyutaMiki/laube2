import pytest
from sqlalchemy.orm import Session
from app.models.models import Users
from app.daos.users_dao import UsersDao
from datetime import datetime, date, time


@pytest.fixture
def users_dict():
    return {
        "id": 1,
        "user_uuid": 'dummy',
        "user_name": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_users(db_session: Session, users_dict):
    dao = UsersDao()
    obj = dao.create(db_session, users_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_users(db_session: Session, users_dict):
    dao = UsersDao()
    obj = dao.create(db_session, users_dict)
    dao.update(db_session, obj.id, {"user_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.user_uuid == "updated"

def test_delete_users(db_session: Session, users_dict):
    dao = UsersDao()
    obj = dao.create(db_session, users_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None