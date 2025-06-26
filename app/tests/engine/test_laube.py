import pytest
from unittest.mock import MagicMock
from app.engine.laube import Laube
from app.models.models import ApplicationForm, ApplicationFormRoute, Boss
from app.models.specifiedValue import RouteFlag
from app.exception.laubeException import LaubeException

def mock_application_form(route_flag):
    return ApplicationForm(
        tenant_uuid="t1",
        application_form_code="FORM1",
        route_flag=route_flag
    )

def mock_application_form_route(individual_route_code):
    return ApplicationFormRoute(
        tenant_uuid="t1",
        application_form_code="FORM1",
        group_code="G1",
        individual_route_code=individual_route_code
    )

def mock_boss():
    return Boss(
        tenant_uuid="t1",
        group_code="G1",
        user_uuid="U1",
        application_form_code="FORM1"
    )

@pytest.fixture
def laube_with_mocks():
    laube = Laube()
    laube.application_form_repository.get_by_code = MagicMock()
    laube.application_form_route_repository.get_by_code_and_group = MagicMock()
    laube.boss_repository.get_by_all_keys = MagicMock()
    laube.boss_repository.get_by_group_null = MagicMock()
    laube.boss_repository.get_by_form_null = MagicMock()
    laube.boss_repository.get_by_group_and_form_null = MagicMock()
    return laube

def test_no_individual_route(laube_with_mocks):
    laube_with_mocks.application_form_repository.get_by_code.return_value = mock_application_form(RouteFlag.NO_INDIVIDUAL_ROUTE)
    result = laube_with_mocks.is_display_boss_field("dummy", "t1", "G1", "U1", "FORM1")
    assert result is False

def test_individual_route_with_code(laube_with_mocks):
    laube_with_mocks.application_form_repository.get_by_code.return_value = mock_application_form(RouteFlag.INDIVIDUAL_ROUTE)
    laube_with_mocks.application_form_route_repository.get_by_code_and_group.return_value = mock_application_form_route("ROUTE123")
    result = laube_with_mocks.is_display_boss_field("dummy", "t1", "G1", "U1", "FORM1")
    assert result is False

def test_individual_route_without_code(laube_with_mocks):
    laube_with_mocks.application_form_repository.get_by_code.return_value = mock_application_form(RouteFlag.INDIVIDUAL_ROUTE)
    laube_with_mocks.application_form_route_repository.get_by_code_and_group.side_effect = [None, None]
    result = laube_with_mocks.is_display_boss_field("dummy", "t1", "G1", "U1", "FORM1")
    assert result is False

def test_boss_route_with_no_boss(laube_with_mocks):
    laube_with_mocks.application_form_repository.get_by_code.return_value = mock_application_form(RouteFlag.BOSS_ROUTE)
    laube_with_mocks.boss_repository.get_by_all_keys.return_value = None
    laube_with_mocks.boss_repository.get_by_group_null.return_value = None
    laube_with_mocks.boss_repository.get_by_form_null.return_value = None
    laube_with_mocks.boss_repository.get_by_group_and_form_null.return_value = None
    result = laube_with_mocks.is_display_boss_field("dummy", "t1", "G1", "U1", "FORM1")
    assert result is True

def test_boss_route_with_boss_found(laube_with_mocks):
    laube_with_mocks.application_form_repository.get_by_code.return_value = mock_application_form(RouteFlag.BOSS_ROUTE)
    laube_with_mocks.boss_repository.get_by_all_keys.return_value = mock_boss()
    result = laube_with_mocks.is_display_boss_field("dummy", "t1", "G1", "U1", "FORM1")
    assert result is False

@pytest.mark.parametrize("tenant_uuid, group_code, user_uuid, form_code, expected_code", [
    (None, "G1", "U1", "FORM1", "Laube-E002"),
    ("t1", None, "U1", "FORM1", "Laube-E003"),
    ("t1", "G1", None, "FORM1", "Laube-E004"),
    ("t1", "G1", "U1", None, "Laube-E005"),
])
def test_param_validation_errors(laube_with_mocks, tenant_uuid, group_code, user_uuid, form_code, expected_code):
    laube_with_mocks.error_loader.get_message = MagicMock(return_value="エラーメッセージ")
    with pytest.raises(LaubeException) as excinfo:
        laube_with_mocks.is_display_boss_field("dummy", tenant_uuid, group_code, user_uuid, form_code)
    assert expected_code in str(excinfo.value)

def test_application_form_not_found(laube_with_mocks):
    laube_with_mocks.application_form_repository.get_by_code.return_value = None
    laube_with_mocks.E006 = "Laube-E006"
    with pytest.raises(LaubeException) as excinfo:
        laube_with_mocks.is_display_boss_field("dummy", "t1", "G1", "U1", "FORM1")
    assert "Laube-E006" in str(excinfo.value)


def test_invalid_route_flag(laube_with_mocks):
    laube_with_mocks.application_form_repository.get_by_code.return_value = mock_application_form(999)
    laube_with_mocks.E007 = "Laube-E007"
    with pytest.raises(LaubeException) as excinfo:
        laube_with_mocks.is_display_boss_field("dummy", "t1", "G1", "U1", "FORM1")
    assert "Laube-E007" in str(excinfo.value)


def test_unexpected_exception_wrapped(laube_with_mocks):
    def raise_unexpected(*args, **kwargs):
        raise ZeroDivisionError("division by zero")

    laube_with_mocks.application_form_repository.get_by_code = raise_unexpected

    with pytest.raises(LaubeException) as excinfo:
        laube_with_mocks.is_display_boss_field("dummy", "t1", "G1", "U1", "FORM1")

    assert isinstance(excinfo.value.original_exception, ZeroDivisionError)
