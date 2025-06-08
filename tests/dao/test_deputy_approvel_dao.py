import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import DeputyApprovel
from jp.co.linkpoint.laube.daos.deputy_approvel_dao import DeputyApprovelDao

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
        "create_date": '2024-01-01T00:00:00',
        "create_employee_code": 'dummy',
        "update_date": '2024-01-01T00:00:00',
        "update_employee_code": 'dummy',
        "update_count": 1,
        
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
    dao.delete(db_session, obj.id)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None