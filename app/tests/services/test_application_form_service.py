import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.services.application_form_service import ApplicationFormService
from app.models.models import ApplicationForm
from app.models.specifiedValue import AutoApproverlFlag, PullingFlag, RouteFlag, WithdrawalFlag


@pytest.fixture
def dummy_application_form_dict():
    return {
        "id": 1,
        "tenant_uuid": "dummy-tenant",
        "application_form_code": "FORM001",
        "application_form_name": "休暇申請",
        "application_classification_code": "LEAVE",
        "skip_apply_employee": True,
        "auto_approverl_flag": AutoApproverlFlag.AUTOMATIC_APPROVAL,
        "pulling_flag": PullingFlag.A,
        "withdrawal_flag": WithdrawalFlag.ENABLED,
        "route_flag": RouteFlag.NO_INDIVIDUAL_ROUTE,
        "sort_number": 1,
        "executed_after_approverl": "hook_xxx",
        "table_name": "t_application_leave",
        "screen_code": "SCREEN001",
        "job_title_code": "JT001",
        "create_date": datetime(2024, 1, 1),
        "create_user_uuid": "user-001",
        "update_date": datetime(2024, 1, 1),
        "update_user_uuid": "user-001",
        "update_count": 1
    }


@pytest.fixture
def mock_dao():
    return MagicMock()


@pytest.fixture
def service(mock_dao):
    service = ApplicationFormService()
    service.dao = mock_dao
    return service


def test_create_application_form_service(session, dummy_application_form_dict, service, mock_dao):
    mock_obj = ApplicationForm(**dummy_application_form_dict)
    mock_dao.create.return_value = mock_obj

    result = service.create(session, dummy_application_form_dict)

    assert result.application_form_code == "FORM001"
    mock_dao.create.assert_called_once_with(session, dummy_application_form_dict)


def test_get_application_form_service(session, service, mock_dao):
    mock_obj = ApplicationForm(id=1, application_form_code="FORM001")
    mock_dao.get.return_value = mock_obj

    result = service.get(session, 1)

    assert result.application_form_code == "FORM001"
    mock_dao.get.assert_called_once_with(session, 1)
