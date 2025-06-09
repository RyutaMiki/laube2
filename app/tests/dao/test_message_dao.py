import pytest
from sqlalchemy.orm import Session
from app.models.models import Message
from app.daos.message_dao import MessageDao
from datetime import datetime, date, time


@pytest.fixture
def message_dict():
    return {
        "id": 1,
        "language_code": 'dummy',
        "message_key": 'dummy',
        "message_text": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_message(db_session: Session, message_dict):
    dao = MessageDao()
    obj = dao.create(db_session, message_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_message(db_session: Session, message_dict):
    dao = MessageDao()
    obj = dao.create(db_session, message_dict)
    dao.update(db_session, obj.id, {"language_code": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.language_code == "updated"

def test_delete_message(db_session: Session, message_dict):
    dao = MessageDao()
    obj = dao.create(db_session, message_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None