import pytest
from sqlalchemy.orm import Session
from app.models.models import WorkflowGraphView
from app.daos.workflow_graph_view_dao import WorkflowGraphViewDao
from datetime import datetime, date, time
from app.models.specifiedValue import ApprovalFunction, TransitionType

@pytest.fixture
def workflow_graph_view_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_form_code": 'dummy',
        "route_type": 1,
        "from_activity_code": 1,
        "from_function": ApprovalFunction.EXAMINATION,
        "to_activity_code": 1,
        "to_function": ApprovalFunction.EXAMINATION,
        "transition_type": TransitionType.AND,
        "condition_expression": 'dummy',
        "group_key": 'dummy',
        "sort_number": 1,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_workflow_graph_view(db_session: Session, workflow_graph_view_dict):
    dao = WorkflowGraphViewDao()
    obj = dao.create(db_session, workflow_graph_view_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_workflow_graph_view(db_session: Session, workflow_graph_view_dict):
    dao = WorkflowGraphViewDao()
    obj = dao.create(db_session, workflow_graph_view_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_workflow_graph_view(db_session: Session, workflow_graph_view_dict):
    dao = WorkflowGraphViewDao()
    obj = dao.create(db_session, workflow_graph_view_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None