import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import CommonActivity
from jp.co.linkpoint.laube.daos.common_activity_dao import CommonActivityDao

@pytest.fixture
def common_activity_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "common_route_code": 'dummy',
        "activity_code": 1,
        "approverl_tenant_uuid": 'dummy',
        "approverl_role_code": 'dummy',
        "approverl_group_code": 'dummy',
        "approverl_user_uuid": 'dummy',
        "function": 1,
        "create_date": '2024-01-01T00:00:00',
        "create_employee_code": 'dummy',
        "update_date": '2024-01-01T00:00:00',
        "update_employee_code": 'dummy',
        "update_count": 1,
        
    }

def test_create_and_get_common_activity(db_session: Session, common_activity_dict):
    dao = CommonActivityDao()
    obj = dao.create(db_session, common_activity_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_common_activity(db_session: Session, common_activity_dict):
    dao = CommonActivityDao()
    obj = dao.create(db_session, common_activity_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_common_activity(db_session: Session, common_activity_dict):
    dao = CommonActivityDao()
    obj = dao.create(db_session, common_activity_dict)
    dao.delete(db_session, obj.id)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None