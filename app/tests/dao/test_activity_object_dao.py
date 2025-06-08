import pytest
from sqlalchemy.orm import Session
from app.models.models import ActivityObject
from app.daos.activity_object_dao import ActivityObjectDao
from datetime import datetime, date, time
from app.models.specifiedValue import ActivityStatus, ApprovalFunction

@pytest.fixture
def activity_object_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_number": 1,
        "route_type": 1,
        "route_number": 1,
        "group_key": 'dummy',
        "approverl_tenant_uuid": 'dummy',
        "approverl_role_code": 'dummy',
        "approverl_group_code": 'dummy',
        "approverl_user_uuid": 'dummy',
        "function": ApprovalFunction.EXAMINATION,
        "instance_group_id": 'dummy',
        "instance_index": 1,
        "total_instance_count": 1,
        "loop_count": 1,
        "max_loop": 1,
        "parent_activity_id": 1,
        "is_synchronized": True,
        "is_interleaved_locked": True,
        "is_milestone": True,
        "is_milestone_reached": True,
        "is_canceled": True,
        "cancel_reason": 'dummy',
        "canceled_by": 'dummy',
        "is_terminal": True,
        "is_discriminator_loser": True,
        "is_deferred_choice_winner": True,
        "is_deferred_choice_loser": True,
        "trigger_type": 'dummy',
        "is_triggered": True,
        "triggered_at": datetime(2024, 1, 1, 0, 0, 0),
        "reaching_date": datetime(2024, 1, 1, 0, 0, 0),
        "process_date": datetime(2024, 1, 1, 0, 0, 0),
        "activity_status": ActivityStatus.IN_PROGRESS,
        "approverl_comment": 'dummy',
        "is_completed": True,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_employee_code": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_employee_code": 'dummy',
        "update_count": 1
    }

def test_create_and_get_activity_object(db_session: Session, activity_object_dict):
    dao = ActivityObjectDao()
    obj = dao.create(db_session, activity_object_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_activity_object(db_session: Session, activity_object_dict):
    dao = ActivityObjectDao()
    obj = dao.create(db_session, activity_object_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_activity_object(db_session: Session, activity_object_dict):
    dao = ActivityObjectDao()
    obj = dao.create(db_session, activity_object_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None