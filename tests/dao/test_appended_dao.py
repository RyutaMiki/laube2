import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import Appended
from jp.co.linkpoint.laube.daos.appended_dao import AppendedDao
from datetime import datetime, date, time


@pytest.fixture
def appended_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_number": 1,
        "route_type": 1,
        "route_number": 1,
        "group_key": 'dummy',
        "approverl_tenant_uuid": 'dummy',
        "approverl_group_code": 'dummy',
        "approverl_user_uuid": 'dummy',
        "append_title": 'dummy',
        "append_path": 'dummy',
        "append_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_employee_code": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_employee_code": 'dummy',
        "update_count": 1
    }

def test_create_and_get_appended(db_session: Session, appended_dict):
    dao = AppendedDao()
    obj = dao.create(db_session, appended_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_appended(db_session: Session, appended_dict):
    dao = AppendedDao()
    obj = dao.create(db_session, appended_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_appended(db_session: Session, appended_dict):
    dao = AppendedDao()
    obj = dao.create(db_session, appended_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None