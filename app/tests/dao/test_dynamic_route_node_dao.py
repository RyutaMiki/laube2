import pytest
from sqlalchemy.orm import Session
from app.models.models import DynamicRouteNode
from app.daos.dynamic_route_node_dao import DynamicRouteNodeDao
from datetime import datetime, date, time
from app.models.specifiedValue import ApprovalFunction

@pytest.fixture
def dynamic_route_node_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_number": 1,
        "route_type": 1,
        "route_number": 1,
        "approverl_user_uuid": 'dummy',
        "approverl_group_code": 'dummy',
        "function": ApprovalFunction.EXAMINATION,
        "comment": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_dynamic_route_node(db_session: Session, dynamic_route_node_dict):
    dao = DynamicRouteNodeDao()
    obj = dao.create(db_session, dynamic_route_node_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_dynamic_route_node(db_session: Session, dynamic_route_node_dict):
    dao = DynamicRouteNodeDao()
    obj = dao.create(db_session, dynamic_route_node_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_dynamic_route_node(db_session: Session, dynamic_route_node_dict):
    dao = DynamicRouteNodeDao()
    obj = dao.create(db_session, dynamic_route_node_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None