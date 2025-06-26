import pytest
from sqlalchemy.orm import Session
from app.models.models import Resource
from app.daos.resource_dao import ResourceDao
from datetime import datetime, date, time


@pytest.fixture
def resource_dict():
    return {
        "id": 1,
        "resource_id": 'dummy',
        "resource_name": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_resource(db_session: Session, resource_dict):
    dao = ResourceDao()
    obj = dao.create(db_session, resource_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_resource(db_session: Session, resource_dict):
    dao = ResourceDao()
    obj = dao.create(db_session, resource_dict)
    dao.update(db_session, obj.id, {"resource_id": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.resource_id == "updated"

def test_delete_resource(db_session: Session, resource_dict):
    dao = ResourceDao()
    obj = dao.create(db_session, resource_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None