import pytest
from sqlalchemy.orm import Session
from app.models.models import WorkflowTrigger
from app.daos.workflow_trigger_dao import WorkflowTriggerDao
from datetime import datetime, date, time
from app.models.specifiedValue import InheritMode

@pytest.fixture
def workflow_trigger_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "trigger_form_code": 'dummy',
        "trigger_activity_code": 1,
        "target_form_code": 'dummy',
        "inherit_mode": InheritMode.USER_ONLY,
        "trigger_condition": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_workflow_trigger(db_session: Session, workflow_trigger_dict):
    dao = WorkflowTriggerDao()
    obj = dao.create(db_session, workflow_trigger_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_workflow_trigger(db_session: Session, workflow_trigger_dict):
    dao = WorkflowTriggerDao()
    obj = dao.create(db_session, workflow_trigger_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_workflow_trigger(db_session: Session, workflow_trigger_dict):
    dao = WorkflowTriggerDao()
    obj = dao.create(db_session, workflow_trigger_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None