import pytest
from sqlalchemy.orm import Session
from app.models.models import Boss
from app.daos.boss_dao import BossDao
from datetime import datetime, date, time


@pytest.fixture
def boss_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "user_uuid": 'dummy',
        "group_code": 'dummy',
        "application_form_code": 'dummy',
        "boss_tenant_uuid": 'dummy',
        "boss_group_code": 'dummy',
        "boss_user_uuid": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_boss(db_session: Session, boss_dict):
    dao = BossDao()
    obj = dao.create(db_session, boss_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_boss(db_session: Session, boss_dict):
    dao = BossDao()
    obj = dao.create(db_session, boss_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_boss(db_session: Session, boss_dict):
    dao = BossDao()
    obj = dao.create(db_session, boss_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None