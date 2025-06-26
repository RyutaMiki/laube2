from datetime import date, datetime
from app.models.models import TenantUser

def test_find_active_user(session, tenant_user_repository):
    user = TenantUser(
        tenant_uuid="tenant123",
        user_uuid="user123",
        belong_start_date=date(2024, 1, 1),
        belong_end_date=None,
        create_date=datetime.now(),
        create_user_uuid="test-user",
        update_date=datetime.now(),
        update_user_uuid="test-user",
        update_count=1
    )
    session.add(user)
    session.commit()

    result = tenant_user_repository.find_active_user(
        session,
        "tenant123",
        "user123"
    )

    assert result is not None
    assert result.user_uuid == "user123"
