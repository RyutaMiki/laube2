import pytest
from sqlalchemy.orm import Session
from app.models.models import ApplicationObject
from app.daos.application_object_dao import ApplicationObjectDao
from datetime import datetime, date, time
from app.models.specifiedValue import ApplicationStatus

@pytest.fixture
def application_object_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_number": 1,
        "re_application_number": 1,
        "application_form_code": 'dummy',
        "target_tenant_uuid": 'dummy',
        "target_group_code": 'dummy',
        "target_user_uuid": 'dummy',
        "applicant_tenant_uuid": 'dummy',
        "applicant_group_code": 'dummy',
        "applicant_user_uuid": 'dummy',
        "apply_date": datetime(2024, 1, 1, 0, 0, 0),
        "approval_date": datetime(2024, 1, 1, 0, 0, 0),
        "application_status": ApplicationStatus.DRAFT,
        "is_case_canceled": True,
        "case_cancel_reason": 'dummy',
        "case_canceled_by": 'dummy',
        "total_instance_count": 1,
        "milestone_count": 1,
        "reached_milestone_count": 1,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_application_object(db_session: Session, application_object_dict):
    dao = ApplicationObjectDao()
    obj = dao.create(db_session, application_object_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_application_object(db_session: Session, application_object_dict):
    dao = ApplicationObjectDao()
    obj = dao.create(db_session, application_object_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_application_object(db_session: Session, application_object_dict):
    dao = ApplicationObjectDao()
    obj = dao.create(db_session, application_object_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None