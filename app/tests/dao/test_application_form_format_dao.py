import pytest
from sqlalchemy.orm import Session
from app.models.models import ApplicationFormFormat
from app.daos.application_form_format_dao import ApplicationFormFormatDao
from datetime import datetime, date, time
from app.models.specifiedValue import AutoApproverlFlag, PullingFlag, RouteFlag, WithdrawalFlag

@pytest.fixture
def application_form_format_dict():
    return {
        "id": 1,
        "application_form_code": 'dummy',
        "application_form_name": 'dummy',
        "application_classification_code": 'dummy',
        "skip_apply_employee": True,
        "auto_approverl_flag": AutoApproverlFlag.AUTOMATIC_APPROVAL,
        "pulling_flag": PullingFlag.A,
        "withdrawal_flag": WithdrawalFlag.ENABLED,
        "route_flag": RouteFlag.DIRECT,
        "sort_number": 1,
        "table_name": 'dummy',
        "screen_code": 'dummy',
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_application_form_format(db_session: Session, application_form_format_dict):
    dao = ApplicationFormFormatDao()
    obj = dao.create(db_session, application_form_format_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_application_form_format(db_session: Session, application_form_format_dict):
    dao = ApplicationFormFormatDao()
    obj = dao.create(db_session, application_form_format_dict)
    dao.update(db_session, obj.id, {"application_form_code": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.application_form_code == "updated"

def test_delete_application_form_format(db_session: Session, application_form_format_dict):
    dao = ApplicationFormFormatDao()
    obj = dao.create(db_session, application_form_format_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None