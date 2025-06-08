import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import ActivityTransit
from jp.co.linkpoint.laube.daos.activity_transit_dao import ActivityTransitDao
from datetime import datetime, date, time
from jp.co.linkpoint.laube.daos.base.specifiedValue import ApprovalConditionType, TransitionType

@pytest.fixture
def activity_transit_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_number": 1,
        "from_route_type": 1,
        "from_route_number": 1,
        "to_route_type": 1,
        "to_route_number": 1,
        "transition_type": TransitionType.AND,
        "group_key": 'dummy',
        "condition_expression": 'dummy',
        "approval_condition_type": ApprovalConditionType.ALL,
        "approval_threshold": 1,
        "sort_number": 1,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_employee_code": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_employee_code": 'dummy',
        "update_count": 1
    }

def test_create_and_get_activity_transit(db_session: Session, activity_transit_dict):
    dao = ActivityTransitDao()
    obj = dao.create(db_session, activity_transit_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_activity_transit(db_session: Session, activity_transit_dict):
    dao = ActivityTransitDao()
    obj = dao.create(db_session, activity_transit_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_activity_transit(db_session: Session, activity_transit_dict):
    dao = ActivityTransitDao()
    obj = dao.create(db_session, activity_transit_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None