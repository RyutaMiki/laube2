import pytest
from sqlalchemy.orm import Session
from app.models.models import CommonActivity
from app.daos.common_activity_dao import CommonActivityDao
from datetime import datetime, date, time
from app.models.specifiedValue import ApprovalFunction, ConditionExpressionType, EscalationAction, SkipMode

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
        "function": ApprovalFunction.EXAMINATION,
        "instance_group_id": 'dummy',
        "instance_index": 1,
        "total_instance_count": 1,
        "max_loop": 1,
        "is_synchronized": True,
        "is_interleaved_locked": True,
        "is_milestone": True,
        "is_terminal": True,
        "is_discriminator_loser": True,
        "is_deferred_choice_winner": True,
        "is_deferred_choice_loser": True,
        "trigger_type": 'dummy',
        "timeout_hours": 1,
        "escalation_action": EscalationAction.ESCALATE,
        "escalation_target_user_uuid": 'dummy',
        "condition_expression": 'dummy',
        "condition_type": ConditionExpressionType.DSL,
        "skip_mode": SkipMode.SKIP,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
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
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None