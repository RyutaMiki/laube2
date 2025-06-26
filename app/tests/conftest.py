import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from app.models.models import Base
from app.repositories.individual_activity_repository import IndividualActivityRepository
from app.repositories.tenant_user_repository import TenantUserRepository
from app.repositories.user_group_repository import UserGroupRepository

# エンジンとSessionの定義（テスト全体で使う用）
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def session():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()  # 安全のため rollback
        session.close()
        clear_mappers()  # メモリDBの再作成で警告防止（あれば）

@pytest.fixture
def individual_activity_repository():
    return IndividualActivityRepository()

@pytest.fixture
def tenant_user_repository():
    return TenantUserRepository()

@pytest.fixture
def user_group_repository():
    return UserGroupRepository()
