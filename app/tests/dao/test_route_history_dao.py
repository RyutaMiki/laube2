import pytest
from sqlalchemy.orm import Session
from app.models.models import RouteHistory
from app.daos.route_history_dao import RouteHistoryDao
from datetime import datetime, date, time
from app.models.specifiedValue import ActivityStatus, ApplicantStatus, ApplicationStatus, ApprovalFunction

@pytest.fixture
def route_history_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "group_key": 'dummy',
        "company_name": 'dummy',
        "application_number": 1,
        "re_application_number": 1,
        "application_form_code": 'dummy',
        "application_form_name": 'dummy',
        "target_tenant_uuid": 'dummy',
        "target_company_name": 'dummy',
        "target_group_code": 'dummy',
        "target_group_name": 'dummy',
        "target_user_uuid": 'dummy',
        "target_employee_name": 'dummy',
        "applicant_tenant_uuid": 'dummy',
        "applicant_company_name": 'dummy',
        "applicant_group_code": 'dummy',
        "applicant_group_name": 'dummy',
        "applicant_user_uuid": 'dummy',
        "applicant_employee_name": 'dummy',
        "apply_date": datetime(2024, 1, 1, 0, 0, 0),
        "approval_date": datetime(2024, 1, 1, 0, 0, 0),
        "application_status": ApplicationStatus.DRAFT,
        "applicant_status": ApplicantStatus.NEW,
        "route_type": 1,
        "route_number": 1,
        "approverl_tenant_uuid": 'dummy',
        "approverl_company_name": 'dummy',
        "approverl_role_code": 'dummy',
        "approverl_role_name": 'dummy',
        "approverl_group_code": 'dummy',
        "approverl_group_name": 'dummy',
        "approverl_user_uuid": 'dummy',
        "approverl_employee_name": 'dummy',
        "deputy_approverl_tenant_uuid": 'dummy',
        "deputy_approverl_company_name": 'dummy',
        "deputy_approverl_group_code": 'dummy',
        "deputy_approverl_group_name": 'dummy',
        "deputy_approverl_user_uuid": 'dummy',
        "deputy_approverl_employee_name": 'dummy',
        "deputy_contents": 'dummy',
        "function": ApprovalFunction.EXAMINATION,
        "reaching_date": datetime(2024, 1, 1, 0, 0, 0),
        "process_date": datetime(2024, 1, 1, 0, 0, 0),
        "activity_status": ActivityStatus.IN_PROGRESS,
        "approverl_comment": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_employee_code": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_employee_code": 'dummy',
        "update_count": 1
    }

def test_create_and_get_route_history(db_session: Session, route_history_dict):
    dao = RouteHistoryDao()
    obj = dao.create(db_session, route_history_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_route_history(db_session: Session, route_history_dict):
    dao = RouteHistoryDao()
    obj = dao.create(db_session, route_history_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_route_history(db_session: Session, route_history_dict):
    dao = RouteHistoryDao()
    obj = dao.create(db_session, route_history_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None