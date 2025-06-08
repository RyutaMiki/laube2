import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import Group
from jp.co.linkpoint.laube.daos.group_dao import GroupDao
from datetime import datetime, date, time
from jp.co.linkpoint.laube.daos.base.specifiedValue import PermissionRange

@pytest.fixture
def group_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "group_code": 'dummy',
        "group_name": 'dummy',
        "term_from": date(2024, 1, 1),
        "term_to": date(2024, 1, 1),
        "upper_group_code": 'dummy',
        "permission_range": PermissionRange.ALL,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_employee_code": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_employee_code": 'dummy',
        "update_count": 1
    }

def test_create_and_get_group(db_session: Session, group_dict):
    dao = GroupDao()
    obj = dao.create(db_session, group_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_group(db_session: Session, group_dict):
    dao = GroupDao()
    obj = dao.create(db_session, group_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_group(db_session: Session, group_dict):
    dao = GroupDao()
    obj = dao.create(db_session, group_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None