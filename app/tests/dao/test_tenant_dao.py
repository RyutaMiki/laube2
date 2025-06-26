import pytest
from sqlalchemy.orm import Session
from app.models.models import Tenant
from app.daos.tenant_dao import TenantDao
from datetime import datetime, date, time


@pytest.fixture
def tenant_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_tenant(db_session: Session, tenant_dict):
    dao = TenantDao()
    obj = dao.create(db_session, tenant_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_tenant(db_session: Session, tenant_dict):
    dao = TenantDao()
    obj = dao.create(db_session, tenant_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_tenant(db_session: Session, tenant_dict):
    dao = TenantDao()
    obj = dao.create(db_session, tenant_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None