import pytest
from sqlalchemy.orm import Session
from app.models.models import DeputyApprovel
from app.daos.deputy_approvel_dao import DeputyApprovelDao
from datetime import datetime, date, time


@pytest.fixture
def deputy_approvel_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "group_code": 'dummy',
        "user_uuid": 'dummy',
        "deputy_approverl_tenant_uuid": 'dummy',
        "deputy_approverl_group_code": 'dummy',
        "deputy_approverl_user_uuid": 'dummy',
        "deputy_contents": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_deputy_approvel(db_session: Session, deputy_approvel_dict):
    dao = DeputyApprovelDao()
    obj = dao.create(db_session, deputy_approvel_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_deputy_approvel(db_session: Session, deputy_approvel_dict):
    dao = DeputyApprovelDao()
    obj = dao.create(db_session, deputy_approvel_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_deputy_approvel(db_session: Session, deputy_approvel_dict):
    dao = DeputyApprovelDao()
    obj = dao.create(db_session, deputy_approvel_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None