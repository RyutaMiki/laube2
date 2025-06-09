import pytest
from sqlalchemy.orm import Session
from app.models.models import ApplicationComment
from app.daos.application_comment_dao import ApplicationCommentDao
from datetime import datetime, date, time


@pytest.fixture
def application_comment_dict():
    return {
        "id": 1,
        "tenant_uuid": 'dummy',
        "application_number": 1,
        "parent_comment_id": 1,
        "route_type": 1,
        "route_number": 1,
        "poster_user_uuid": 'dummy',
        "poster_group_code": 'dummy',
        "comment_text": 'dummy',
        "posted_at": datetime(2024, 1, 1, 0, 0, 0),
        "is_deleted": True,
        "create_date": datetime(2024, 1, 1, 0, 0, 0),
        "create_user_uuid": 'dummy',
        "update_date": datetime(2024, 1, 1, 0, 0, 0),
        "update_user_uuid": 'dummy',
        "update_count": 1
    }

def test_create_and_get_application_comment(db_session: Session, application_comment_dict):
    dao = ApplicationCommentDao()
    obj = dao.create(db_session, application_comment_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_application_comment(db_session: Session, application_comment_dict):
    dao = ApplicationCommentDao()
    obj = dao.create(db_session, application_comment_dict)
    dao.update(db_session, obj.id, {"tenant_uuid": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.tenant_uuid == "updated"

def test_delete_application_comment(db_session: Session, application_comment_dict):
    dao = ApplicationCommentDao()
    obj = dao.create(db_session, application_comment_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None