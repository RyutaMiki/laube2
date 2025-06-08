import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import Employee
from jp.co.linkpoint.laube.daos.employee_dao import EmployeeDao

@pytest.fixture
def employee_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "user_uuid": 'dummy',
        "belong_start_date": '2024-01-01',
        "belong_end_date": '2024-01-01',
        "create_date": '2024-01-01T00:00:00',
        "create_user_uuid": 'dummy',
        "update_date": '2024-01-01T00:00:00',
        "update_user_uuid": 'dummy',
        "update_count": 1,
        
    }

def test_create_and_get_employee(db_session: Session, employee_dict):
    dao = EmployeeDao()
    obj = dao.create(db_session, employee_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_employee(db_session: Session, employee_dict):
    dao = EmployeeDao()
    obj = dao.create(db_session, employee_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_employee(db_session: Session, employee_dict):
    dao = EmployeeDao()
    obj = dao.create(db_session, employee_dict)
    dao.delete(db_session, obj.id)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None