import pytest
from sqlalchemy.orm import Session
from app.models.models import EmployeeGroup
from app.daos.employee_group_dao import EmployeeGroupDao
from datetime import datetime, date, time
from app.models.specifiedValue import DefaultGroupFlg, Range

@pytest.fixture
def employee_group_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "user_uuid": 'dummy',
        "group_code": 'dummy',
        "default_group_code": DefaultGroupFlg.ON,
        "term_from": date(2024, 1, 1),
        "term_to": date(2024, 1, 1),
        "range": Range.PERSONAL,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_employee_code": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_employee_code": 'dummy',
        "update_count": 1
    }

def test_create_and_get_employee_group(db_session: Session, employee_group_dict):
    dao = EmployeeGroupDao()
    obj = dao.create(db_session, employee_group_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_employee_group(db_session: Session, employee_group_dict):
    dao = EmployeeGroupDao()
    obj = dao.create(db_session, employee_group_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_employee_group(db_session: Session, employee_group_dict):
    dao = EmployeeGroupDao()
    obj = dao.create(db_session, employee_group_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None