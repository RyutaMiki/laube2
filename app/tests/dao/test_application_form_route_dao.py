import pytest
from sqlalchemy.orm import Session
from app.models.models import ApplicationFormRoute
from app.daos.application_form_route_dao import ApplicationFormRouteDao
from datetime import datetime, date, time


@pytest.fixture
def application_form_route_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_form_code": 'dummy',
        "group_code": 'dummy',
        "individual_route_code": 'dummy',
        "common_route_code": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_application_form_route(db_session: Session, application_form_route_dict):
    dao = ApplicationFormRouteDao()
    obj = dao.create(db_session, application_form_route_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_application_form_route(db_session: Session, application_form_route_dict):
    dao = ApplicationFormRouteDao()
    obj = dao.create(db_session, application_form_route_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_application_form_route(db_session: Session, application_form_route_dict):
    dao = ApplicationFormRouteDao()
    obj = dao.create(db_session, application_form_route_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None