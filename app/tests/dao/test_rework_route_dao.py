import pytest
from sqlalchemy.orm import Session
from app.models.models import ReworkRoute
from app.daos.rework_route_dao import ReworkRouteDao
from datetime import datetime, date, time


@pytest.fixture
def rework_route_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_form_code": 'dummy',
        "from_route_type": 1,
        "from_route_number": 1,
        "to_route_type": 1,
        "to_route_number": 1,
        "condition_expression": 'dummy',
        "comment": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_rework_route(db_session: Session, rework_route_dict):
    dao = ReworkRouteDao()
    obj = dao.create(db_session, rework_route_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_rework_route(db_session: Session, rework_route_dict):
    dao = ReworkRouteDao()
    obj = dao.create(db_session, rework_route_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_rework_route(db_session: Session, rework_route_dict):
    dao = ReworkRouteDao()
    obj = dao.create(db_session, rework_route_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None