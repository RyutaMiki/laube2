import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base
from app.repositories.individual_activity_repository import IndividualActivityRepository
from app.repositories.tenant_user_repository import TenantUserRepository
from app.repositories.user_group_repository import UserGroupRepository

# ✅ エンジンは1回だけ作成（sessionスコープ）
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """全体のテスト実行前にテーブル作成"""
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """各テストで独立したセッションを使用"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# 以下は repository を必要とするテスト向け
@pytest.fixture
def individual_activity_repository():
    return IndividualActivityRepository()

@pytest.fixture
def tenant_user_repository():
    return TenantUserRepository()

@pytest.fixture
def user_group_repository():
    return UserGroupRepository()
