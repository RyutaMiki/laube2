
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, Date, TIMESTAMP, DECIMAL,
    Index, UniqueConstraint, ForeignKey, ForeignKeyConstraint,
    PrimaryKeyConstraint, CheckConstraint, text, func, SmallInteger
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import uuid
from jp.co.linkpoint.laube.daos.base.enumType import EnumType
from jp.co.linkpoint.laube.daos.base.specifiedValue import *
Base = declarative_base()


class Users(Base):
    """
    　実在する利用者（人）を一意に管理するテーブル
    """
    __tablename__ = 'm_users'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    user_uuid = Column('user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, unique=True, default="lambda: str(uuid.uuid4())", comment="ユーザーUUID")
    user_name = Column('user_name', String(50, collation='ja_JP.utf8'), nullable=False, comment="氏名")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now", comment="作成日時")
    create_user_uuid = Column('create_user_uuid', String(10, collation='ja_JP.utf8'), nullable=False, comment="作成者ユーザーコード")
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now, comment="更新日時")
    update_user_uuid = Column('update_user_uuid', String(10, collation='ja_JP.utf8'), nullable=False, comment="更新者ユーザーコード")
    update_count = Column('update_count', Integer, nullable=False, comment="更新回数")


class Tenants(Base):
    """
    　会社ごとのテナント情報
    """
    __tablename__ = 'm_tenants'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, unique=True, default="lambda: str(uuid.uuid4())", comment="テナントUUID")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now", comment="作成日時")
    create_user_uuid = Column('create_user_uuid', String(10, collation='ja_JP.utf8'), nullable=False, comment="作成者ユーザーコード")
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now, comment="更新日時")
    update_user_uuid = Column('update_user_uuid', String(10, collation='ja_JP.utf8'), nullable=False, comment="更新者ユーザーコード")
    update_count = Column('update_count', Integer, nullable=False, comment="更新回数")


class Employee(Base):
    """
    　会社ごとにどのユーザーが所属しているか管理
    　同じユーザーが再入社した場合は新しいレコードを追加し、履歴を保持する
    """
    __tablename__ = 'employees'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    user_uuid = Column('user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="ユーザーUUID")
    belong_start_date = Column('belong_start_date', Date, nullable=False, comment="所属開始日")
    belong_end_date = Column('belong_end_date', Date, nullable=True, comment="所属終了日（現役中はNULL）")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now", comment="作成日時")
    create_user_uuid = Column('create_user_uuid', String(10, collation='ja_JP.utf8'), nullable=False, comment="作成者ユーザーコード")
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now, comment="更新日時")
    update_user_uuid = Column('update_user_uuid', String(10, collation='ja_JP.utf8'), nullable=False, comment="更新者ユーザーコード")
    update_count = Column('update_count', Integer, nullable=False, comment="更新回数")
    __table_args__ = (
        ForeignKeyConstraint(['user_uuid'], ['m_users.user_uuid']),
        ForeignKeyConstraint(['tenant_uuid'], ['m_tenants.tenant_uuid']),
        UniqueConstraint('tenant_uuid', 'user_uuid', 'belong_start_date')
    )

class Boss(Base):
    """
    　上司マスタ
    """
    __tablename__ = 'm_boss'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    user_uuid = Column('user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="ユーザーUUID")
    group_code = Column('group_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="部署コード")
    application_form_code = Column('application_form_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="申請書コード")
    boss_tenant_uuid = Column('boss_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="直属上司のテナントUUID")
    boss_group_code = Column('boss_group_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="直属上司の部署コード")
    boss_user_uuid = Column('boss_user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="直属上司のユーザーUUID")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_boss_tenant_uuid_group_code_user_uuid_application_form_code', tenant_uuid, group_code, user_uuid, application_form_code),
        Index('ix_m_boss', tenant_uuid),
        UniqueConstraint(tenant_uuid, group_code, user_uuid, application_form_code)
    )

class DeputyApprovel(Base):
    """
    　代理承認者マスタ
    """
    __tablename__ = 'm_deputy_approvel'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    group_code = Column('group_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="部署コード")
    user_uuid = Column('user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="ユーザーUUID")
    deputy_approverl_tenant_uuid = Column('deputy_approverl_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="代理承認者のテナントUUID")
    deputy_approverl_group_code = Column('deputy_approverl_group_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="代理承認者の部署コード")
    deputy_approverl_user_uuid = Column('deputy_approverl_user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="代理承認者のユーザーUUID")
    deputy_contents = Column('deputy_contents', String(255, collation='ja_JP.utf8'), nullable=False, comment="依頼理由")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_deputy_approvel_tenant_uuid_group_code_user_uuid', tenant_uuid, group_code, user_uuid),
        Index('ix_m_deputy_approvel', tenant_uuid),
        UniqueConstraint(tenant_uuid, group_code, user_uuid)
    )

class ApplicationClassificationFormat(Base):
    """
    　規定申請分類マスタ
    """
    __tablename__ = 'm_application_classification_format'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    application_classification_code = Column('application_classification_code', String(10, collation='ja_JP.utf8'), nullable=False, unique=True, comment="申請分類コード")
    application_classification_name = Column('application_classification_name', String(30, collation='ja_JP.utf8'), nullable=False, comment="申請分類名")
    sort_number = Column('sort_number', Integer, nullable=False, comment="ソート順")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_application_classification_format', application_classification_code),
        UniqueConstraint(application_classification_code)
    )

class ApplicationFormFormat(Base):
    """
    　規定申請書マスタ
    """
    __tablename__ = 'm_application_form_format'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    application_form_code = Column('application_form_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="申請書コード")
    application_form_name = Column('application_form_name', String(30, collation='ja_JP.utf8'), nullable=False, comment="申請書名")
    application_classification_code = Column('application_classification_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="申請分類コード")
    skip_apply_employee = Column('skip_apply_employee', Boolean, nullable=False, comment="申請者を承認から外す判定")
    auto_approverl_flag = Column('auto_approverl_flag', EnumType(enum_class=AutoApproverlFlag), nullable=False, comment="自動承認フラグ")
    pulling_flag = Column('pulling_flag', EnumType(enum_class=PullingFlag), nullable=False, comment="引き戻し区分")
    withdrawal_flag = Column('withdrawal_flag', EnumType(enum_class=WithdrawalFlag), nullable=False, comment="取り下げ区分")
    route_flag = Column('route_flag', EnumType(enum_class=RouteFlag), nullable=False, comment="直接部門の扱い")
    sort_number = Column('sort_number', Integer, nullable=False, comment="ソート順")
    table_name = Column('table_name', String(50, collation='ja_JP.utf8'), nullable=False, unique=True, comment="テーブル名")
    screen_code = Column('screen_code', String(6, collation='ja_JP.utf8'), nullable=False, comment="画面コード")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_application_form_format', application_form_code),
        UniqueConstraint(application_form_code)
    )

class ApplicationForm(Base):
    """
    　申請書マスタ
    """
    __tablename__ = 'm_application_form'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    application_form_code = Column('application_form_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="申請書コード")
    application_form_name = Column('application_form_name', String(30, collation='ja_JP.utf8'), nullable=False, comment="申請書名")
    application_classification_code = Column('application_classification_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="申請分類コード")
    skip_apply_employee = Column('skip_apply_employee', Boolean, nullable=False, comment="申請者を承認から外す判定")
    auto_approverl_flag = Column('auto_approverl_flag', EnumType(enum_class=AutoApproverlFlag), nullable=False, comment="自動承認フラグ")
    pulling_flag = Column('pulling_flag', EnumType(enum_class=PullingFlag), nullable=False, comment="引き戻し区分")
    withdrawal_flag = Column('withdrawal_flag', EnumType(enum_class=WithdrawalFlag), nullable=False, comment="取り下げ区分")
    route_flag = Column('route_flag', EnumType(enum_class=RouteFlag), nullable=False, comment="直接部門の扱い")
    sort_number = Column('sort_number', Integer, nullable=False, comment="ソート順")
    executed_after_approverl = Column('executed_after_approverl', String(255, collation='ja_JP.utf8'), nullable=True, comment="承認後に実行するタスク")
    table_name = Column('table_name', String(50, collation='ja_JP.utf8'), nullable=False, comment="テーブル名")
    screen_code = Column('screen_code', String(6, collation='ja_JP.utf8'), nullable=False, comment="画面コード")
    job_title_code = Column('job_title_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="役職コード")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_application_form_tenant_uuid_application_form_code', tenant_uuid, application_form_code),
        Index('ix_m_application_form', tenant_uuid),
        Index('ix_m_application_form', application_form_code),
        UniqueConstraint(tenant_uuid, application_form_code),
        UniqueConstraint(tenant_uuid, application_form_name),
        UniqueConstraint(tenant_uuid, table_name)
    )

class ApplicationFormRoute(Base):
    """
    　申請書別ルートマスタ
    """
    __tablename__ = 'm_application_form_route'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    application_form_code = Column('application_form_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="申請書コード")
    group_code = Column('group_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="部署コード")
    individual_route_code = Column('individual_route_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="直接部門")
    common_route_code = Column('common_route_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="間接部門")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_application_form_route_tenant_uuid_application_form_code_group_code', tenant_uuid, application_form_code, group_code),
        Index('ix_m_application_form_route', tenant_uuid),
        UniqueConstraint(tenant_uuid, application_form_code, group_code)
    )

class IndividualRoute(Base):
    """
    　直接ルートマスタ
    """
    __tablename__ = 'm_individual_route'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    individual_route_code = Column('individual_route_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="直接部門")
    individual_route_name = Column('individual_route_name', String(30, collation='ja_JP.utf8'), nullable=False, comment="直接部門名")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_individual_route_tenant_uuid_individual_route_code', tenant_uuid, individual_route_code),
        Index('ix_m_individual_route', tenant_uuid),
        UniqueConstraint(tenant_uuid, individual_route_code),
        UniqueConstraint(tenant_uuid, individual_route_name)
    )

class IndividualActivity(Base):
    """
    　直接ルートアクティビティマスタ
    """
    __tablename__ = 'm_individual_activity'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    individual_route_code = Column('individual_route_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="直接部門コード")
    activity_code = Column('activity_code', Integer, nullable=False, comment="アクティビティコード")
    approverl_ctenant_uuid = Column('approverl_ctenant_uuid', String(10, collation='ja_JP.utf8'), nullable=True, comment="承認者のテナントUUID")
    approverl_role_code = Column('approverl_role_code', String(30, collation='ja_JP.utf8'), nullable=True, comment="承認者の利用権限コード")
    approverl_group_code = Column('approverl_group_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="承認者の部署コード")
    approverl_user_uuid = Column('approverl_user_uuid', String(10, collation='ja_JP.utf8'), nullable=True, comment="承認者のユーザーUUID")
    function = Column('function', EnumType(enum_class=ApprovalFunction), nullable=False, comment="承認画面の機能")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_individual_activity_tenant_uuid_individual_route_code_activity_code', tenant_uuid, individual_route_code, activity_code),
        Index('ix_m_individual_activity_tenant_uuid_individual_route_code', tenant_uuid, individual_route_code),
        Index('ix_m_individual_activity_tenant_uuid_approverl_role_code', tenant_uuid, approverl_role_code),
        Index('ix_m_individual_activity', tenant_uuid),
        UniqueConstraint(tenant_uuid, individual_route_code, activity_code)
    )

class CommonRoute(Base):
    """
    　間接ルートマスタ
    """
    __tablename__ = 'm_common_route'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    common_route_code = Column('common_route_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="間接部門")
    common_route_name = Column('common_route_name', String(30, collation='ja_JP.utf8'), nullable=False, comment="間接部門名")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_common_route_tenant_uuid_common_route_code', tenant_uuid, common_route_code),
        Index('ix_m_common_route', tenant_uuid),
        UniqueConstraint(tenant_uuid, common_route_code),
        UniqueConstraint(tenant_uuid, common_route_name)
    )

class CommonActivity(Base):
    """
    　間接ルートアクティビティマスタ
    """
    __tablename__ = 'm_common_activity'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    common_route_code = Column('common_route_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="間接部門コード")
    activity_code = Column('activity_code', Integer, nullable=False, comment="アクティビティコード")
    approverl_tenant_uuid = Column('approverl_tenant_uuid', String(10, collation='ja_JP.utf8'), nullable=True, comment="承認者のテナントUUID")
    approverl_role_code = Column('approverl_role_code', String(30, collation='ja_JP.utf8'), nullable=True, comment="承認者の利用権限コード")
    approverl_group_code = Column('approverl_group_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="承認者の部署コード")
    approverl_user_uuid = Column('approverl_user_uuid', String(10, collation='ja_JP.utf8'), nullable=True, comment="承認者のユーザーUUID")
    function = Column('function', EnumType(enum_class=ApprovalFunction), nullable=False, comment="承認画面の機能")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_m_common_activity_tenant_uuid_common_route_code_activity_code', tenant_uuid, common_route_code, activity_code),
        Index('ix_m_common_activity_tenant_uuid_common_route_code', tenant_uuid, common_route_code),
        Index('ix_m_common_activity_tenant_uuid_approverl_role_code', tenant_uuid, approverl_role_code),
        Index('ix_m_common_activity', tenant_uuid),
        UniqueConstraint(tenant_uuid, common_route_code, activity_code)
    )

class ApplicationObject(Base):
    """
    　申請オブジェクト
    """
    __tablename__ = 't_application_object'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="申請番号")
    re_application_number = Column('re_application_number', Integer, nullable=True, comment="旧申請番号")
    application_form_code = Column('application_form_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="申請書コード")
    target_tenant_uuid = Column('target_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="対象者のテナントUUID")
    target_group_code = Column('target_group_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="対象者の部署コード")
    target_user_uuid = Column('target_user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="対象者のユーザーUUID")
    applicant_tenant_uuid = Column('applicant_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="申請者のテナントUUID")
    applicant_group_code = Column('applicant_group_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="申請者の部署コード")
    applicant_user_uuid = Column('applicant_user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="申請者のユーザーUUID")
    apply_date = Column('apply_date', TIMESTAMP, nullable=False, comment="申請日")
    approval_date = Column('approval_date', TIMESTAMP, nullable=True, comment="承認日")
    application_status = Column('application_status', EnumType(enum_class=ApplicationStatus), nullable=False, comment="申請書状態")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_t_application_object_tenant_uuid_application_number', tenant_uuid, application_number),
        Index('ix_t_application_object', tenant_uuid),
        UniqueConstraint(tenant_uuid, application_number)
    )

class ActivityObject(Base):
    """
    　申請明細オブジェクト
    """
    __tablename__ = 't_activity_object'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="申請番号")
    route_type = Column('route_type', Integer, nullable=False, comment="ルートタイプ")
    route_number = Column('route_number', Integer, nullable=False, comment="ルートナンバー")
    group_key = Column('group_key', String(20, collation='ja_JP.utf8'), nullable=True, comment="分岐グループ識別子")
    approverl_tenant_uuid = Column('approverl_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="承認者のテナントUUID")
    approverl_role_code = Column('approverl_role_code', String(30, collation='ja_JP.utf8'), nullable=True, comment="承認者の利用権限コード")
    approverl_group_code = Column('approverl_group_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="承認者の部署コード")
    approverl_user_uuid = Column('approverl_user_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="承認者のユーザーUUID")
    deputy_approverl_tenant_uuid = Column('deputy_approverl_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="代理承認者のテナントUUID")
    deputy_approverl_group_code = Column('deputy_approverl_group_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="代理承認者の部署コード")
    deputy_approverl_user_uuid = Column('deputy_approverl_user_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="代理承認者のユーザーUUID")
    deputy_contents = Column('deputy_contents', String(255, collation='ja_JP.utf8'), nullable=True, comment="依頼理由")
    function = Column('function', EnumType(enum_class=ApprovalFunction), nullable=False, comment="承認画面の機能")
    reaching_date = Column('reaching_date', TIMESTAMP, nullable=True, comment="到達日")
    process_date = Column('process_date', TIMESTAMP, nullable=True, comment="処理日")
    activity_status = Column('activity_status', EnumType(enum_class=ActivityStatus), nullable=True, comment="承認者状態")
    approverl_comment = Column('approverl_comment', String(255, collation='ja_JP.utf8'), nullable=True, comment="承認者のコメント")
    is_completed = Column('is_completed', Boolean, nullable=False, comment="アクティビティの完了状態（trueなら完了）")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_t_activity_object_tenant_uuid_application_number_route_type_route_number_approverl_tenant_uuid_approverl_group_code_approverl_user_uuid', tenant_uuid, application_number, route_type, route_number, approverl_tenant_uuid, approverl_group_code, approverl_user_uuid),
        Index('ix_t_activity_object', tenant_uuid),
        Index('ix_t_activity_object_tenant_uuid_application_number', tenant_uuid, application_number),
        UniqueConstraint(tenant_uuid, application_number, route_type, route_number, approverl_tenant_uuid, approverl_group_code, approverl_user_uuid)
    )

class Appended(Base):
    """
    　添付オブジェクト
    """
    __tablename__ = 't_appended'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="申請番号")
    route_type = Column('route_type', Integer, nullable=False, comment="ルートタイプ")
    route_number = Column('route_number', Integer, nullable=False, comment="ルートナンバー")
    group_key = Column('group_key', String(20, collation='ja_JP.utf8'), nullable=True, comment="分岐グループ識別子")
    approverl_tenant_uuid = Column('approverl_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="承認者のテナントUUID")
    approverl_group_code = Column('approverl_group_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="承認者の部署コード")
    approverl_user_uuid = Column('approverl_user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="承認者のユーザーUUID")
    append_title = Column('append_title', String(255, collation='ja_JP.utf8'), nullable=False, comment="添付ファイルの説明")
    append_path = Column('append_path', String(255, collation='ja_JP.utf8'), nullable=False, comment="添付ファイルのパス")
    append_date = Column('append_date', TIMESTAMP, nullable=False, comment="添付ファイルの登録日")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
    __table_args__ = (
        Index('ix_t_appended_tenant_uuid_application_number_route_type_route_number', tenant_uuid, application_number, route_type, route_number),
        Index('ix_t_appended', tenant_uuid),
        Index('ix_t_appended_tenant_uuid_application_number', tenant_uuid, application_number),
        UniqueConstraint(tenant_uuid, application_number, route_type, route_number)
    )

class RouteHistory(Base):
    """
    　申請書履歴オブジェクト
    """
    __tablename__ = 't_route_history'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    group_key = Column('group_key', String(20, collation='ja_JP.utf8'), nullable=True, comment="分岐グループ識別子")
    company_name = Column('company_name', String(50, collation='ja_JP.utf8'), nullable=False, comment="会社名")
    application_number = Column('application_number', Integer, nullable=False, comment="申請番号")
    re_application_number = Column('re_application_number', Integer, nullable=True, comment="旧申請番号")
    application_form_code = Column('application_form_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="申請書コード")
    application_form_name = Column('application_form_name', String(30, collation='ja_JP.utf8'), nullable=False, comment="申請書名")
    target_tenant_uuid = Column('target_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="対象者のテナントUUID")
    target_company_name = Column('target_company_name', String(50, collation='ja_JP.utf8'), nullable=False, comment="対象者の会社名")
    target_group_code = Column('target_group_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="対象者の部署コード")
    target_group_name = Column('target_group_name', String(50, collation='ja_JP.utf8'), nullable=False, comment="対象者の部署名")
    target_user_uuid = Column('target_user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="対象者のユーザーUUID")
    target_employee_name = Column('target_employee_name', String(30, collation='ja_JP.utf8'), nullable=False, comment="対象者の氏名")
    applicant_tenant_uuid = Column('applicant_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="申請者のテナントUUID")
    applicant_company_name = Column('applicant_company_name', String(50, collation='ja_JP.utf8'), nullable=False, comment="申請者の会社名")
    applicant_group_code = Column('applicant_group_code', String(10, collation='ja_JP.utf8'), nullable=False, comment="申請者の部署コード")
    applicant_group_name = Column('applicant_group_name', String(50, collation='ja_JP.utf8'), nullable=False, comment="申請者の部署名")
    applicant_user_uuid = Column('applicant_user_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="申請者のユーザーUUID")
    applicant_employee_name = Column('applicant_employee_name', String(30, collation='ja_JP.utf8'), nullable=False, comment="申請者の氏名")
    apply_date = Column('apply_date', TIMESTAMP, nullable=False, comment="申請日")
    approval_date = Column('approval_date', TIMESTAMP, nullable=True, comment="承認日")
    application_status = Column('application_status', EnumType(enum_class=ApplicationStatus), nullable=False, comment="申請書状態")
    applicant_status = Column('applicant_status', EnumType(enum_class=ApplicantStatus), nullable=True, comment="申請者状態")
    route_type = Column('route_type', Integer, nullable=True, comment="ルートタイプ")
    route_number = Column('route_number', Integer, nullable=True, comment="ルートナンバー")
    approverl_tenant_uuid = Column('approverl_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="承認者のテナントUUID")
    approverl_company_name = Column('approverl_company_name', String(50, collation='ja_JP.utf8'), nullable=True, comment="承認者の会社名")
    approverl_role_code = Column('approverl_role_code', String(30, collation='ja_JP.utf8'), nullable=True, comment="承認者の利用権限コード")
    approverl_role_name = Column('approverl_role_name', String(30, collation='ja_JP.utf8'), nullable=True, comment="承認者の利用権限名")
    approverl_group_code = Column('approverl_group_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="承認者の部署コード")
    approverl_group_name = Column('approverl_group_name', String(50, collation='ja_JP.utf8'), nullable=True, comment="承認者の部署名")
    approverl_user_uuid = Column('approverl_user_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="承認者のユーザーUUID")
    approverl_employee_name = Column('approverl_employee_name', String(30, collation='ja_JP.utf8'), nullable=True, comment="承認者氏名")
    deputy_approverl_tenant_uuid = Column('deputy_approverl_tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="代理承認者のテナントUUID")
    deputy_approverl_company_name = Column('deputy_approverl_company_name', String(50, collation='ja_JP.utf8'), nullable=True, comment="代理承認者の会社名")
    deputy_approverl_group_code = Column('deputy_approverl_group_code', String(10, collation='ja_JP.utf8'), nullable=True, comment="代理承認者の部署コード")
    deputy_approverl_group_name = Column('deputy_approverl_group_name', String(50, collation='ja_JP.utf8'), nullable=True, comment="代理承認者の部署名")
    deputy_approverl_user_uuid = Column('deputy_approverl_user_uuid', String(36, collation='ja_JP.utf8'), nullable=True, comment="代理承認者のユーザーUUID")
    deputy_approverl_employee_name = Column('deputy_approverl_employee_name', String(30, collation='ja_JP.utf8'), nullable=True, comment="代理承認者氏名")
    deputy_contents = Column('deputy_contents', String(255, collation='ja_JP.utf8'), nullable=True, comment="依頼理由")
    function = Column('function', EnumType(enum_class=ApprovalFunction), nullable=True, comment="承認画面の機能")
    reaching_date = Column('reaching_date', TIMESTAMP, nullable=True, comment="到達日")
    process_date = Column('process_date', TIMESTAMP, nullable=True, comment="処理日")
    activity_status = Column('activity_status', EnumType(enum_class=ActivityStatus), nullable=True, comment="承認者状態")
    approverl_comment = Column('approverl_comment', String(255, collation='ja_JP.utf8'), nullable=True, comment="承認者のコメント")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }


class ActivityTransit(Base):
    """
    　アクティビティ遷移定義（AND/OR/条件分岐）
    """
    __tablename__ = 't_activity_transit'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36, collation='ja_JP.utf8'), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="対象申請番号")
    from_route_type = Column('from_route_type', Integer, nullable=False, comment="遷移元ルートタイプ")
    from_route_number = Column('from_route_number', Integer, nullable=False, comment="遷移元ルートナンバー")
    to_route_type = Column('to_route_type', Integer, nullable=False, comment="遷移先ルートタイプ")
    to_route_number = Column('to_route_number', Integer, nullable=False, comment="遷移先ルートナンバー")
    transition_type = Column('transition_type', EnumType(enum_class=TransitionType), nullable=False, comment="遷移タイプ（AND/OR/CONDITION）")
    group_key = Column('group_key', String(20, collation='ja_JP.utf8'), nullable=True, comment="分岐グループキー")
    condition_expression = Column('condition_expression', String(255, collation='ja_JP.utf8'), nullable=True, comment="条件式（JSONやDSL）")
    approval_condition_type = Column('approval_condition_type', EnumType(enum_class=ApprovalConditionType), nullable=False, default="ALL", comment="承認完了条件の種別（ALL=全員, MAJORITY=過半数, ANY=誰か1人）")
    approval_threshold = Column('approval_threshold', Integer, nullable=True, comment="任意人数承認で可とする場合の閾値（approval_condition_type='THRESHOLD'時）")
    sort_number = Column('sort_number', Integer, nullable=True, comment="並び順")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default="datetime.now")
    create_employee_code = Column('create_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default="datetime.now", onupdate=datetime.now)
    update_employee_code = Column('update_employee_code', String(10, collation='ja_JP.utf8'), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)
    __mapper_args__ = {
        'version_id_col': "update_count"    }
