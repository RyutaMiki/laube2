import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import CommonRoute
from jp.co.linkpoint.laube.daos.common_route_dao import CommonRouteDao

@pytest.fixture
def common_route_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "common_route_code": 'dummy',
        "common_route_name": 'dummy',
        "create_date": '2024-01-01T00:00:00',
        "create_employee_code": 'dummy',
        "update_date": '2024-01-01T00:00:00',
        "update_employee_code": 'dummy',
        "update_count": 1,
        
    }

def test_create_and_get_common_route(db_session: Session, common_route_dict):
    dao = CommonRouteDao()
    obj = dao.create(db_session, common_route_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_common_route(db_session: Session, common_route_dict):
    dao = CommonRouteDao()
    obj = dao.create(db_session, common_route_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_common_route(db_session: Session, common_route_dict):
    dao = CommonRouteDao()
    obj = dao.create(db_session, common_route_dict)
    dao.delete(db_session, obj.id)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None