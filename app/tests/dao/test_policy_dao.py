import pytest
from sqlalchemy.orm import Session
from app.models.models import Policy
from app.daos.policy_dao import PolicyDao
from datetime import datetime, date, time


@pytest.fixture
def policy_dict():
    return {
        "id": 1,
        "policy_id": 'dummy',
        "role_id": 'dummy',
        "permission_id": 'dummy',
        "resource_id": 'dummy',
        "condition": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_policy(db_session: Session, policy_dict):
    dao = PolicyDao()
    obj = dao.create(db_session, policy_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_policy(db_session: Session, policy_dict):
    dao = PolicyDao()
    obj = dao.create(db_session, policy_dict)
    dao.update(db_session, obj.id, {"policy_id": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.policy_id == "updated"

def test_delete_policy(db_session: Session, policy_dict):
    dao = PolicyDao()
    obj = dao.create(db_session, policy_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None