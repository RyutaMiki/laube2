import pytest
from sqlalchemy.orm import Session
from app.models.models import TenantUser
from app.daos.tenant_user_dao import TenantUserDao
from datetime import datetime, date, time


@pytest.fixture
def tenant_user_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "user_uuid": 'dummy',
        "belong_start_date": date(2024, 1, 1),
        "belong_end_date": date(2024, 1, 1),
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_tenant_user(db_session: Session, tenant_user_dict):
    dao = TenantUserDao()
    obj = dao.create(db_session, tenant_user_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_tenant_user(db_session: Session, tenant_user_dict):
    dao = TenantUserDao()
    obj = dao.create(db_session, tenant_user_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_tenant_user(db_session: Session, tenant_user_dict):
    dao = TenantUserDao()
    obj = dao.create(db_session, tenant_user_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None