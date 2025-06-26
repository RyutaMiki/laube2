import pytest
from sqlalchemy.orm import Session
from app.models.models import User
from app.daos.user_dao import UserDao
from datetime import datetime, date, time


@pytest.fixture
def user_dict():
    return {
        "id": 1,
        "user_uuid": 'dummy',
        "user_name": 'dummy',
        "hashed_password": 'dummy',
        "is_active": True,
        "last_login_at": datetime(2024, 1, 1, 0, 0, 0),
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_user(db_session: Session, user_dict):
    dao = UserDao()
    obj = dao.create(db_session, user_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_user(db_session: Session, user_dict):
    dao = UserDao()
    obj = dao.create(db_session, user_dict)
    dao.update(db_session, obj.id, {"user_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.user_uuid == "updated"

def test_delete_user(db_session: Session, user_dict):
    dao = UserDao()
    obj = dao.create(db_session, user_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None