import pytest
from sqlalchemy.orm import Session
from app.models.models import Tenants
from app.daos.tenants_dao import TenantsDao
from datetime import datetime, date, time


@pytest.fixture
def tenants_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_tenants(db_session: Session, tenants_dict):
    dao = TenantsDao()
    obj = dao.create(db_session, tenants_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_tenants(db_session: Session, tenants_dict):
    dao = TenantsDao()
    obj = dao.create(db_session, tenants_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_tenants(db_session: Session, tenants_dict):
    dao = TenantsDao()
    obj = dao.create(db_session, tenants_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None