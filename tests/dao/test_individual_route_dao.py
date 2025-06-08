import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import IndividualRoute
from jp.co.linkpoint.laube.daos.individual_route_dao import IndividualRouteDao
from datetime import datetime, date, time


@pytest.fixture
def individual_route_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "individual_route_code": 'dummy',
        "individual_route_name": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_employee_code": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_employee_code": 'dummy',
        "update_count": 1
    }

def test_create_and_get_individual_route(db_session: Session, individual_route_dict):
    dao = IndividualRouteDao()
    obj = dao.create(db_session, individual_route_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_individual_route(db_session: Session, individual_route_dict):
    dao = IndividualRouteDao()
    obj = dao.create(db_session, individual_route_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_individual_route(db_session: Session, individual_route_dict):
    dao = IndividualRouteDao()
    obj = dao.create(db_session, individual_route_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None