from datetime import datetime
from app.models.models import IndividualActivity
from app.models.specifiedValue import ApprovalFunction

def test_find_by_tenant_and_route(db_session, individual_activity_repository):
    activity = IndividualActivity(
        tenant_uuid="abc",
        individual_route_code="ROUTE001",
        activity_code="A001",
        function=ApprovalFunction.EXAMINATION,
        create_date=datetime.now(),
        update_date=datetime.now(),
        create_user_uuid="test-user",
        update_user_uuid="test-user",
        update_count=1
    )
    db_session.add(activity)
    db_session.commit()

    results = individual_activity_repository.find_by_tenant_and_route(
        db_session,
        "abc",
        "ROUTE001",
        "A001"
    )

    assert len(results) == 1
    assert results[0].individual_route_code == "ROUTE001"
    assert results[0].activity_code == "A001"
