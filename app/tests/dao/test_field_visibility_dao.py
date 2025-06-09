import pytest
from sqlalchemy.orm import Session
from app.models.models import FieldVisibility
from app.daos.field_visibility_dao import FieldVisibilityDao
from datetime import datetime, date, time
from app.models.specifiedValue import FieldVisibilityType

@pytest.fixture
def field_visibility_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_form_code": 'dummy',
        "activity_code": 1,
        "field_name": 'dummy',
        "visibility": FieldVisibilityType.VISIBLE,
        "editable_by_applicant": True,
        "editable_by_approver": True,
        "comment": 'dummy',
        "label_key": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_field_visibility(db_session: Session, field_visibility_dict):
    dao = FieldVisibilityDao()
    obj = dao.create(db_session, field_visibility_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_field_visibility(db_session: Session, field_visibility_dict):
    dao = FieldVisibilityDao()
    obj = dao.create(db_session, field_visibility_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_field_visibility(db_session: Session, field_visibility_dict):
    dao = FieldVisibilityDao()
    obj = dao.create(db_session, field_visibility_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None