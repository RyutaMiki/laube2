import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import ApplicationForm
from jp.co.linkpoint.laube.daos.application_form_dao import ApplicationFormDao

@pytest.fixture
def application_form_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_form_code": 'dummy',
        "application_form_name": 'dummy',
        "application_classification_code": 'dummy',
        "skip_apply_employee": True,
        "auto_approverl_flag": 1,
        "pulling_flag": 1,
        "withdrawal_flag": 1,
        "route_flag": 1,
        "sort_number": 1,
        "executed_after_approverl": 'dummy',
        "table_name": 'dummy',
        "screen_code": 'dummy',
        "job_title_code": 'dummy',
        "create_date": '2024-01-01T00:00:00',
        "create_employee_code": 'dummy',
        "update_date": '2024-01-01T00:00:00',
        "update_employee_code": 'dummy',
        "update_count": 1,
        
    }

def test_create_and_get_application_form(db_session: Session, application_form_dict):
    dao = ApplicationFormDao()
    obj = dao.create(db_session, application_form_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_application_form(db_session: Session, application_form_dict):
    dao = ApplicationFormDao()
    obj = dao.create(db_session, application_form_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_application_form(db_session: Session, application_form_dict):
    dao = ApplicationFormDao()
    obj = dao.create(db_session, application_form_dict)
    dao.delete(db_session, obj.id)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None