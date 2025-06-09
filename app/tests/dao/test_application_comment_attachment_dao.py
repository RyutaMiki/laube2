import pytest
from sqlalchemy.orm import Session
from app.models.models import ApplicationCommentAttachment
from app.daos.application_comment_attachment_dao import ApplicationCommentAttachmentDao
from datetime import datetime, date, time


@pytest.fixture
def application_comment_attachment_dict():
    return {
        "id": 1,
        "comment_id": 1,
        "file_name": 'dummy',
        "file_path": 'dummy'
    }

def test_create_and_get_application_comment_attachment(db_session: Session, application_comment_attachment_dict):
    dao = ApplicationCommentAttachmentDao()
    obj = dao.create(db_session, application_comment_attachment_dict)
    found = dao.get(db_session, obj.id)
    assert found is not None

def test_update_application_comment_attachment(db_session: Session, application_comment_attachment_dict):
    dao = ApplicationCommentAttachmentDao()
    obj = dao.create(db_session, application_comment_attachment_dict)
    dao.update(db_session, obj.id, {"comment_id": "updated"})
    updated = dao.get(db_session, obj.id)
    assert updated.comment_id == "updated"

def test_delete_application_comment_attachment(db_session: Session, application_comment_attachment_dict):
    dao = ApplicationCommentAttachmentDao()
    obj = dao.create(db_session, application_comment_attachment_dict)
    dao.delete(db_session, obj)
    deleted = dao.get(db_session, obj.id)
    assert deleted is None