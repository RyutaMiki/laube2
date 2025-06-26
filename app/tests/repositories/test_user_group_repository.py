from datetime import date, datetime
import pytest
from app.models.models import UserGroup
from app.models.specifiedValue import DefaultGroupFlg, Range  # ← Enum忘れずに！

@pytest.fixture
def user_group_repository():
    from app.repositories.user_group_repository import UserGroupRepository
    return UserGroupRepository()

def test_find_by_keys(session, user_group_repository):
    group = UserGroup(
        tenant_uuid="t001",
        user_uuid="u001",
        group_code="G001",
        default_group_code=DefaultGroupFlg.ON,  # Enum インスタンスを渡すこと！
        term_from=date(2024, 1, 1),
        term_to=None,
        range=Range.PERSONAL,  # これも Enum インスタンス
        create_date=datetime.now(),
        create_user_uuid="test-user",
        update_date=datetime.now(),
        update_user_uuid="test-user",
        update_count=1
    )
    session.add(group)
    session.commit()

    result = user_group_repository.find_by_keys(session, "t001", "u001", "G001")

    assert result is not None
    assert result.group_code == "G001"
