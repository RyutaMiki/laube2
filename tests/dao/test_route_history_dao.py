import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import RouteHistory
from jp.co.linkpoint.laube.daos.route_history_dao import RouteHistoryDao

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
        "apply_date": '2024-01-01T00:00:00',
        "approval_date": '2024-01-01T00:00:00',
        "application_status": 1,
        "applicant_status": 1,
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
        "function": 1,
        "reaching_date": '2024-01-01T00:00:00',
        "process_date": '2024-01-01T00:00:00',
        "activity_status": 1,
        "approverl_comment": 'dummy',
        "create_date": '2024-01-01T00:00:00',
        "create_employee_code": 'dummy',
        "update_date": '2024-01-01T00:00:00',
        "update_employee_code": 'dummy',
        "update_count": 1,
        
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
    dao.delete(db_session, obj.id)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None