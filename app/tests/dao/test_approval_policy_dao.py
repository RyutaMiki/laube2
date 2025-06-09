import pytest
from sqlalchemy.orm import Session
from app.models.models import ApprovalPolicy
from app.daos.approval_policy_dao import ApprovalPolicyDao
from datetime import datetime, date, time
from app.models.specifiedValue import RouteType

@pytest.fixture
def approval_policy_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_form_code": 'dummy',
        "policy_expression": 'dummy',
        "route_override_code": 'dummy',
        "route_type": RouteType.INDIVIDUAL,
        "priority": 1,
        "is_active": True,
        "comment": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_approval_policy(db_session: Session, approval_policy_dict):
    dao = ApprovalPolicyDao()
    obj = dao.create(db_session, approval_policy_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_approval_policy(db_session: Session, approval_policy_dict):
    dao = ApprovalPolicyDao()
    obj = dao.create(db_session, approval_policy_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_approval_policy(db_session: Session, approval_policy_dict):
    dao = ApprovalPolicyDao()
    obj = dao.create(db_session, approval_policy_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None