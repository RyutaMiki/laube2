import pytest
from sqlalchemy.orm import Session
from jp.co.linkpoint.laube.daos.base.models import ApplicationClassificationFormat
from jp.co.linkpoint.laube.daos.application_classification_format_dao import ApplicationClassificationFormatDao
from datetime import datetime, date, time


@pytest.fixture
def application_classification_format_dict():
    return {
        "id": 1,
        "application_classification_code": 'dummy',
        "application_classification_name": 'dummy',
        "sort_number": 1,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_employee_code": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_employee_code": 'dummy',
        "update_count": 1
    }

def test_create_and_get_application_classification_format(db_session: Session, application_classification_format_dict):
    dao = ApplicationClassificationFormatDao()
    obj = dao.create(db_session, application_classification_format_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_application_classification_format(db_session: Session, application_classification_format_dict):
    dao = ApplicationClassificationFormatDao()
    obj = dao.create(db_session, application_classification_format_dict)
    dao.update(db_session, obj.id, {"application_classification_code": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.application_classification_code == "updated"

def test_delete_application_classification_format(db_session: Session, application_classification_format_dict):
    dao = ApplicationClassificationFormatDao()
    obj = dao.create(db_session, application_classification_format_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None