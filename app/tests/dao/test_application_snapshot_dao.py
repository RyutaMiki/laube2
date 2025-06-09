import pytest
from sqlalchemy.orm import Session
from app.models.models import ApplicationSnapshot
from app.daos.application_snapshot_dao import ApplicationSnapshotDao
from datetime import datetime, date, time


@pytest.fixture
def application_snapshot_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_number": 1,
        "version_number": 1,
        "snapshot_data": 'dummy',
        "snapshot_reason": 'dummy',
        "revert_to_version": 1,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_application_snapshot(db_session: Session, application_snapshot_dict):
    dao = ApplicationSnapshotDao()
    obj = dao.create(db_session, application_snapshot_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_application_snapshot(db_session: Session, application_snapshot_dict):
    dao = ApplicationSnapshotDao()
    obj = dao.create(db_session, application_snapshot_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_application_snapshot(db_session: Session, application_snapshot_dict):
    dao = ApplicationSnapshotDao()
    obj = dao.create(db_session, application_snapshot_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None