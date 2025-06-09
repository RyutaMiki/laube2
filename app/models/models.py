
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, Date, TIMESTAMP, DECIMAL,
    Index, UniqueConstraint, ForeignKey, ForeignKeyConstraint,
    PrimaryKeyConstraint, CheckConstraint, text, func, SmallInteger
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import uuid
from app.models.enum_type import EnumType
from app.models.specifiedValue import *
Base = declarative_base()



class Users(Base):
    """
    　実在する利用者（人）を一意に管理するテーブル
    """

    __tablename__ = 'm_users'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    user_uuid = Column('user_uuid', String(36), nullable=False, unique=True, default=uuid.uuid4, comment="ユーザーUUID")
    user_name = Column('user_name', String(50), nullable=False, comment="氏名")
    hashed_password = Column('hashed_password', String(255), nullable=False, comment="ハッシュ化されたパスワード")
    is_active = Column('is_active', Boolean, nullable=False, default=True, comment="利用可能フラグ（無効化対応）")
    last_login_at = Column('last_login_at', TIMESTAMP, nullable=True, comment="最終ログイン日時")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now, comment="作成日時")
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False, comment="作成者ユーザーコード")
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新日時")
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False, comment="更新者ユーザーコード")
    update_count = Column('update_count', Integer, nullable=False, default=0, comment="更新回数")






class Tenants(Base):
    """
    　会社ごとのテナント情報
    """

    __tablename__ = 'm_tenants'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, unique=True, default=uuid.uuid4, comment="テナントUUID")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now, comment="作成日時")
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False, comment="作成者ユーザーコード")
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新日時")
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False, comment="更新者ユーザーコード")
    update_count = Column('update_count', Integer, nullable=False, comment="更新回数")






class Employee(Base):
    """
    　会社ごとにどのユーザーが所属しているか管理
    　同じユーザーが再入社した場合は新しいレコードを追加し、履歴を保持する
    """

    __tablename__ = 'employees'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    user_uuid = Column('user_uuid', String(36), nullable=False, comment="ユーザーUUID")
    belong_start_date = Column('belong_start_date', Date, nullable=False, comment="所属開始日")
    belong_end_date = Column('belong_end_date', Date, nullable=True, comment="所属終了日（現役中はNULL）")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now, comment="作成日時")
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False, comment="作成者ユーザーコード")
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新日時")
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False, comment="更新者ユーザーコード")
    update_count = Column('update_count', Integer, nullable=False, comment="更新回数")




    __table_args__ = (
        ForeignKeyConstraint(['user_uuid'], ['m_users.user_uuid']),
        ForeignKeyConstraint(['tenant_uuid'], ['m_tenants.tenant_uuid']),
        UniqueConstraint('tenant_uuid', 'user_uuid', 'belong_start_date'),
    )

class Group(Base):
    """
    　部署マスタ
    """

    __tablename__ = 'm_group'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    group_code = Column('group_code', String(10), nullable=False, comment="部署コード")
    group_name = Column('group_name', String(50), nullable=False, comment="部署名")
    term_from = Column('term_from', Date, nullable=False, comment="有効開始日")
    term_to = Column('term_to', Date, nullable=True, comment="有効終了日")
    upper_group_code = Column('upper_group_code', String(10), nullable=True, comment="上位部署コード")
    permission_range = Column('permission_range', EnumType(enum_class=PermissionRange), nullable=False, comment="利用権限範囲")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=lambda: datetime.now())
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_m_grouptenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, group_code),
    )

class EmployeeGroup(Base):
    """
    　従業員部署マスタ
    """

    __tablename__ = 'm_employee_group'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    user_uuid = Column('user_uuid', String(36), nullable=False, comment="ユーザーUUID")
    group_code = Column('group_code', String(10), nullable=False, comment="部署コード")
    default_group_code = Column('default_group_code', EnumType(enum_class=DefaultGroupFlg), nullable=True, comment="規定部署コード")
    term_from = Column('term_from', Date, nullable=False, comment="有効開始日")
    term_to = Column('term_to', Date, nullable=True, comment="有効終了日")
    range = Column('range', EnumType(enum_class=Range), nullable=False, comment="利用権限範囲")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_m_employee_grouptenant_uuid_user_uuid_group_code', tenant_uuid, user_uuid, group_code),
        Index('ix_m_employee_grouptenant_uuid', tenant_uuid),
        Index('ix_m_employee_groupuser_uuid', user_uuid),
        Index('ix_m_employee_groupgroup_code', group_code),
        UniqueConstraint(tenant_uuid, user_uuid, group_code),
    )

class Boss(Base):
    """
    　上司マスタ
    """

    __tablename__ = 'm_boss'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    user_uuid = Column('user_uuid', String(36), nullable=False, comment="ユーザーUUID")
    group_code = Column('group_code', String(10), nullable=True, comment="部署コード")
    application_form_code = Column('application_form_code', String(10), nullable=True, comment="申請書コード")
    boss_tenant_uuid = Column('boss_tenant_uuid', String(36), nullable=False, comment="直属上司のテナントUUID")
    boss_group_code = Column('boss_group_code', String(10), nullable=False, comment="直属上司の部署コード")
    boss_user_uuid = Column('boss_user_uuid', String(36), nullable=False, comment="直属上司のユーザーUUID")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_m_bosstenant_uuid_group_code_user_uuid_application_form_code', tenant_uuid, group_code, user_uuid, application_form_code),
        Index('ix_m_bosstenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, group_code, user_uuid, application_form_code),
    )

class DeputyApprovel(Base):
    """
    　代理承認者マスタ
    """

    __tablename__ = 'm_deputy_approvel'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    group_code = Column('group_code', String(10), nullable=False, comment="部署コード")
    user_uuid = Column('user_uuid', String(36), nullable=False, comment="ユーザーUUID")
    deputy_approverl_tenant_uuid = Column('deputy_approverl_tenant_uuid', String(36), nullable=True, comment="代理承認者のテナントUUID")
    deputy_approverl_group_code = Column('deputy_approverl_group_code', String(10), nullable=False, comment="代理承認者の部署コード")
    deputy_approverl_user_uuid = Column('deputy_approverl_user_uuid', String(36), nullable=False, comment="代理承認者のユーザーUUID")
    deputy_contents = Column('deputy_contents', String(255), nullable=False, comment="依頼理由")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_m_deputy_approveltenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, group_code, user_uuid),
    )

class ApplicationClassificationFormat(Base):
    """
    　規定申請分類マスタ
    """

    __tablename__ = 'm_application_classification_format'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    application_classification_code = Column('application_classification_code', String(10), nullable=False, unique=True, comment="申請分類コード")
    application_classification_name = Column('application_classification_name', String(30), nullable=False, comment="申請分類名")
    sort_number = Column('sort_number', Integer, nullable=False, comment="ソート順")
    individual_route_code = Column('individual_route_code', String(10), nullable=False, comment="直接部門")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }



class ApplicationFormFormat(Base):
    """
    　規定申請書マスタ
    """

    __tablename__ = 'm_application_form_format'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    application_form_code = Column('application_form_code', String(10), nullable=False, comment="申請書コード")
    application_form_name = Column('application_form_name', String(30), nullable=False, comment="申請書名")
    application_classification_code = Column('application_classification_code', String(10), nullable=False, comment="申請分類コード")
    skip_apply_employee = Column('skip_apply_employee', Boolean, nullable=False, comment="申請者を承認から外す判定")
    auto_approverl_flag = Column('auto_approverl_flag', EnumType(enum_class=AutoApproverlFlag), nullable=False, comment="自動承認フラグ")
    pulling_flag = Column('pulling_flag', EnumType(enum_class=PullingFlag), nullable=False, comment="引き戻し区分")
    withdrawal_flag = Column('withdrawal_flag', EnumType(enum_class=WithdrawalFlag), nullable=False, comment="取り下げ区分")
    route_flag = Column('route_flag', EnumType(enum_class=RouteFlag), nullable=False, comment="直接部門の扱い")
    sort_number = Column('sort_number', Integer, nullable=False, comment="ソート順")
    table_name = Column('table_name', String(50), nullable=False, unique=True, comment="テーブル名")
    screen_code = Column('screen_code', String(6), nullable=False, comment="画面コード")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }



class ApplicationForm(Base):
    """
    　申請書マスタ
    """

    __tablename__ = 'm_application_form'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_form_code = Column('application_form_code', String(10), nullable=False, comment="申請書コード")
    application_form_name = Column('application_form_name', String(30), nullable=False, comment="申請書名")
    application_classification_code = Column('application_classification_code', String(10), nullable=False, comment="申請分類コード")
    skip_apply_employee = Column('skip_apply_employee', Boolean, nullable=False, comment="申請者を承認から外す判定")
    auto_approverl_flag = Column('auto_approverl_flag', EnumType(enum_class=AutoApproverlFlag), nullable=False, comment="自動承認フラグ")
    pulling_flag = Column('pulling_flag', EnumType(enum_class=PullingFlag), nullable=False, comment="引き戻し区分")
    withdrawal_flag = Column('withdrawal_flag', EnumType(enum_class=WithdrawalFlag), nullable=False, comment="取り下げ区分")
    route_flag = Column('route_flag', EnumType(enum_class=RouteFlag), nullable=False, comment="直接部門の扱い")
    sort_number = Column('sort_number', Integer, nullable=False, comment="ソート順")
    executed_after_approverl = Column('executed_after_approverl', String(255), nullable=True, comment="承認後に実行するタスク")
    table_name = Column('table_name', String(50), nullable=False, comment="テーブル名")
    screen_code = Column('screen_code', String(6), nullable=False, comment="画面コード")
    job_title_code = Column('job_title_code', String(10), nullable=True, comment="役職コード")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_m_application_formtenant_uuid', tenant_uuid),
        Index('ix_m_application_formapplication_form_code', application_form_code),
        UniqueConstraint(tenant_uuid, application_form_code),
        UniqueConstraint(tenant_uuid, application_form_name),
        UniqueConstraint(tenant_uuid, table_name),
    )

class ApplicationFormRoute(Base):
    """
    　申請書別ルートマスタ
    """

    __tablename__ = 'm_application_form_route'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_form_code = Column('application_form_code', String(10), nullable=False, comment="申請書コード")
    group_code = Column('group_code', String(10), nullable=True, comment="部署コード")
    individual_route_code = Column('individual_route_code', String(10), nullable=True, comment="直接部門")
    common_route_code = Column('common_route_code', String(10), nullable=True, comment="間接部門")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_m_application_form_routetenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, application_form_code, group_code),
    )

class IndividualRoute(Base):
    """
    　直接ルートマスタ
    """

    __tablename__ = 'm_individual_route'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    individual_route_code = Column('individual_route_code', String(10), nullable=False, comment="直接部門")
    individual_route_name = Column('individual_route_name', String(30), nullable=False, comment="直接部門名")
    total_instance_count = Column('total_instance_count', Integer, nullable=True, comment="多重インスタンスの総数（全体制御用）")
    milestone_count = Column('milestone_count', Integer, nullable=True, comment="マイルストーンの合計数")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_m_individual_routetenant_uuid_individual_route_code', tenant_uuid, individual_route_code),
        Index('ix_m_individual_routetenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, individual_route_code),
        UniqueConstraint(tenant_uuid, individual_route_name),
    )

class IndividualActivity(Base):
    """
    　直接ルートアクティビティマスタ
    """

    __tablename__ = 'm_individual_activity'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    individual_route_code = Column('individual_route_code', String(10), nullable=False, comment="直接部門コード")
    activity_code = Column('activity_code', Integer, nullable=False, comment="アクティビティコード")
    approverl_tenant_uuid = Column('approverl_tenant_uuid', String(36), nullable=True, comment="承認者のテナントUUID")
    approverl_role_code = Column('approverl_role_code', String(30), nullable=True, comment="承認者の利用権限コード")
    approverl_group_code = Column('approverl_group_code', String(10), nullable=True, comment="承認者の部署コード")
    approverl_user_uuid = Column('approverl_user_uuid', String(36), nullable=True, comment="承認者のユーザーUUID")
    function = Column('function', EnumType(enum_class=ApprovalFunction), nullable=False, comment="承認画面の機能")
    instance_group_id = Column('instance_group_id', String, nullable=True, comment="多重インスタンスグループID")
    instance_index = Column('instance_index', Integer, nullable=True, comment="インスタンス内の番号")
    total_instance_count = Column('total_instance_count', Integer, nullable=True, comment="インスタンスグループ全体の数")
    max_loop = Column('max_loop', Integer, nullable=True, comment="ループ最大回数")
    is_synchronized = Column('is_synchronized', Boolean, nullable=False, default=False, comment="同期必須ならTrue")
    is_interleaved_locked = Column('is_interleaved_locked', Boolean, nullable=False, default=False, comment="並列経路で他が実行中ならTrue")
    is_milestone = Column('is_milestone', Boolean, nullable=False, default=False, comment="マイルストーンとして設定されているか")
    is_terminal = Column('is_terminal', Boolean, nullable=False, default=False, comment="終了ノードとして設定されているか")
    is_discriminator_loser = Column('is_discriminator_loser', Boolean, nullable=False, default=False, comment="Discriminatorで負ける側の経路に設定されているか")
    is_deferred_choice_winner = Column('is_deferred_choice_winner', Boolean, nullable=False, default=False, comment="Deferred Choiceで勝者となる条件に設定されているか")
    is_deferred_choice_loser = Column('is_deferred_choice_loser', Boolean, nullable=False, default=False, comment="Deferred Choiceで敗者となる経路に設定されているか")
    trigger_type = Column('trigger_type', String(50), nullable=True, comment="トリガー種別（イベント名や条件式）")
    timeout_hours = Column('timeout_hours', Integer, nullable=True, comment="指定時間内に処理されない場合のタイムアウト時間（単位：時間）")
    escalation_action = Column('escalation_action', EnumType(enum_class=EscalationAction), nullable=True, comment="タイムアウト時に自動実行されるアクション（ESCALATE / SKIP / APPROVE / RETURN）")
    escalation_target_user_uuid = Column('escalation_target_user_uuid', String(36), nullable=True, comment="エスカレーション先のユーザーUUID（ESCALATE時のみ有効）")
    condition_expression = Column('condition_expression', String(255), nullable=True, comment="実行条件式（申請情報などに基づくスキップ・有効判定式）")
    condition_type = Column('condition_type', EnumType(enum_class=ConditionExpressionType), nullable=True, comment="条件式の評価エンジン種別（DSL / JSONLOGIC / JMESPATHなど）")
    skip_mode = Column('skip_mode', EnumType(enum_class=SkipMode), nullable=True, comment="条件を満たさないときの動作（SKIP=スキップ, BLOCK=中断, WARN=警告のみ）")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_m_individual_activitytenant_uuid_individual_route_code', tenant_uuid, individual_route_code),
        Index('ix_m_individual_activitytenant_uuid_approverl_role_code', tenant_uuid, approverl_role_code),
        Index('ix_m_individual_activitytenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, individual_route_code, activity_code),
    )

class CommonRoute(Base):
    """
    　間接ルートマスタ
    """

    __tablename__ = 'm_common_route'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    common_route_code = Column('common_route_code', String(10), nullable=False, comment="間接部門")
    common_route_name = Column('common_route_name', String(30), nullable=False, comment="間接部門名")
    total_instance_count = Column('total_instance_count', Integer, nullable=True, comment="多重インスタンスの総数（全体制御用）")
    milestone_count = Column('milestone_count', Integer, nullable=True, comment="マイルストーンの合計数")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_m_common_routetenant_uuid_common_route_code', tenant_uuid, common_route_code),
        Index('ix_m_common_routetenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, common_route_code),
        UniqueConstraint(tenant_uuid, common_route_name),
    )

class CommonActivity(Base):
    """
    　間接ルートアクティビティマスタ
    """

    __tablename__ = 'm_common_activity'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    common_route_code = Column('common_route_code', String(10), nullable=False, comment="間接部門コード")
    activity_code = Column('activity_code', Integer, nullable=False, comment="アクティビティコード")
    approverl_tenant_uuid = Column('approverl_tenant_uuid', String(36), nullable=True, comment="承認者のテナントUUID")
    approverl_role_code = Column('approverl_role_code', String(30), nullable=True, comment="承認者の利用権限コード")
    approverl_group_code = Column('approverl_group_code', String(10), nullable=True, comment="承認者の部署コード")
    approverl_user_uuid = Column('approverl_user_uuid', String(36), nullable=True, comment="承認者のユーザーUUID")
    function = Column('function', EnumType(enum_class=ApprovalFunction), nullable=False, comment="承認画面の機能")
    instance_group_id = Column('instance_group_id', String, nullable=True, comment="多重インスタンスグループID")
    instance_index = Column('instance_index', Integer, nullable=True, comment="インスタンス内の番号")
    total_instance_count = Column('total_instance_count', Integer, nullable=True, comment="インスタンスグループ全体の数")
    max_loop = Column('max_loop', Integer, nullable=True, comment="ループ最大回数")
    is_synchronized = Column('is_synchronized', Boolean, nullable=False, default=False, comment="同期必須ならTrue")
    is_interleaved_locked = Column('is_interleaved_locked', Boolean, nullable=False, default=False, comment="並列経路で他が実行中ならTrue")
    is_milestone = Column('is_milestone', Boolean, nullable=False, default=False, comment="マイルストーンとして設定されているか")
    is_terminal = Column('is_terminal', Boolean, nullable=False, default=False, comment="終了ノードとして設定されているか")
    is_discriminator_loser = Column('is_discriminator_loser', Boolean, nullable=False, default=False, comment="Discriminatorで負ける側の経路に設定されているか")
    is_deferred_choice_winner = Column('is_deferred_choice_winner', Boolean, nullable=False, default=False, comment="Deferred Choiceで勝者となる条件に設定されているか")
    is_deferred_choice_loser = Column('is_deferred_choice_loser', Boolean, nullable=False, default=False, comment="Deferred Choiceで敗者となる経路に設定されているか")
    trigger_type = Column('trigger_type', String(50), nullable=True, comment="トリガー種別（イベント名や条件式）")
    timeout_hours = Column('timeout_hours', Integer, nullable=True, comment="指定時間内に処理されない場合のタイムアウト時間（単位：時間）")
    escalation_action = Column('escalation_action', EnumType(enum_class=EscalationAction), nullable=True, comment="タイムアウト時に自動実行されるアクション（ESCALATE / SKIP / APPROVE / RETURN）")
    escalation_target_user_uuid = Column('escalation_target_user_uuid', String(36), nullable=True, comment="エスカレーション先のユーザーUUID（ESCALATE時のみ有効）")
    condition_expression = Column('condition_expression', String(255), nullable=True, comment="実行条件式（申請情報などに基づくスキップ・有効判定式）")
    condition_type = Column('condition_type', EnumType(enum_class=ConditionExpressionType), nullable=True, comment="条件式の評価エンジン種別（DSL / JSONLOGIC / JMESPATHなど）")
    skip_mode = Column('skip_mode', EnumType(enum_class=SkipMode), nullable=True, comment="条件を満たさないときの動作（SKIP=スキップ, BLOCK=中断, WARN=警告のみ）")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_m_common_activitytenant_uuid_common_route_code_activity_code', tenant_uuid, common_route_code, activity_code),
        Index('ix_m_common_activitytenant_uuid_common_route_code', tenant_uuid, common_route_code),
        Index('ix_m_common_activitytenant_uuid_approverl_role_code', tenant_uuid, approverl_role_code),
        Index('ix_m_common_activitytenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, common_route_code, activity_code),
    )

class ApplicationObject(Base):
    """
    　申請オブジェクト（申請全体の状態・多重インスタンス/マイルストーン/キャンセル等も管理）
    """

    __tablename__ = 't_application_object'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="申請番号")
    re_application_number = Column('re_application_number', Integer, nullable=False, comment="旧_申請番号")
    application_form_code = Column('application_form_code', String(10), nullable=False, comment="申請書コード")
    target_tenant_uuid = Column('target_tenant_uuid', String(36), nullable=True, comment="対象者のテナントUUID")
    target_group_code = Column('target_group_code', String(10), nullable=False, comment="対象者の部署コード")
    target_user_uuid = Column('target_user_uuid', String(36), nullable=False, comment="対象者のユーザーUUID")
    applicant_tenant_uuid = Column('applicant_tenant_uuid', String(36), nullable=True, comment="申請者のテナントUUID")
    applicant_group_code = Column('applicant_group_code', String(10), nullable=False, comment="申請者の部署コード")
    applicant_user_uuid = Column('applicant_user_uuid', String(36), nullable=False, comment="申請者のユーザーUUID")
    apply_date = Column('apply_date', TIMESTAMP, nullable=False, comment="申請日")
    approval_date = Column('approval_date', TIMESTAMP, nullable=True, comment="承認日")
    application_status = Column('application_status', EnumType(enum_class=ApplicationStatus), nullable=False, comment="申請書状態")
    is_case_canceled = Column('is_case_canceled', Boolean, nullable=False, default=False, comment="ケース全体（申請全体）がキャンセルされた場合True")
    case_cancel_reason = Column('case_cancel_reason', String(255), nullable=True, comment="ケースキャンセル理由")
    case_canceled_by = Column('case_canceled_by', String(36), nullable=True, comment="キャンセル操作ユーザーUUID")
    total_instance_count = Column('total_instance_count', Integer, nullable=True, comment="多重インスタンスの総数（全体制御用）")
    milestone_count = Column('milestone_count', Integer, nullable=True, comment="マイルストーンの合計数")
    reached_milestone_count = Column('reached_milestone_count', Integer, nullable=True, comment="到達済みマイルストーン数")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_t_application_objecttenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, application_number),
    )

class ActivityObject(Base):
    """
    　申請明細オブジェクト（全WFパターン対応・全状態管理フラグ入り）
    """

    __tablename__ = 't_activity_object'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="申請番号")
    route_type = Column('route_type', Integer, nullable=False, comment="ルートタイプ")
    route_number = Column('route_number', Integer, nullable=False, comment="ルートナンバー")
    group_key = Column('group_key', String(20), nullable=True, comment="分岐グループ識別子")
    approverl_tenant_uuid = Column('approverl_tenant_uuid', String(36), nullable=True, comment="承認者のテナントUUID")
    approverl_role_code = Column('approverl_role_code', String(30), nullable=True, comment="承認者の利用権限コード")
    approverl_group_code = Column('approverl_group_code', String(10), nullable=True, comment="承認者の部署コード")
    approverl_user_uuid = Column('approverl_user_uuid', String(36), nullable=True, comment="承認者のユーザーUUID")
    function = Column('function', EnumType(enum_class=ApprovalFunction), nullable=False, comment="承認画面の機能")
    deputy_approverl_tenant_uuid = Column('deputy_approverl_tenant_uuid', String(36), nullable=True, comment="代理承認者のテナントUUID")
    deputy_approverl_group_code = Column('deputy_approverl_group_code', String(10), nullable=True, comment="代理承認者の部署コード")
    deputy_approverl_user_uuid = Column('deputy_approverl_user_uuid', String(36), nullable=True, comment="代理承認者のユーザーUUID")
    deputy_contents = Column('deputy_contents', String(255), nullable=True, comment="依頼理由")
    instance_group_id = Column('instance_group_id', String, nullable=True, comment="多重インスタンスグループID")
    instance_index = Column('instance_index', Integer, nullable=True, comment="インスタンス内の番号")
    total_instance_count = Column('total_instance_count', Integer, nullable=True, comment="インスタンスグループ全体の数（Activity単位で必要な場合）")
    loop_count = Column('loop_count', Integer, nullable=False, default=0, comment="ループ通過回数")
    max_loop = Column('max_loop', Integer, nullable=True, comment="ループ最大回数")
    parent_activity_id = Column('parent_activity_id', Integer, nullable=True, comment="再帰元アクティビティID")
    is_synchronized = Column('is_synchronized', Boolean, nullable=False, default=False, comment="同期必須ならTrue")
    is_interleaved_locked = Column('is_interleaved_locked', Boolean, nullable=False, default=False, comment="並列経路で他が実行中ならTrue")
    is_milestone = Column('is_milestone', Boolean, nullable=False, default=False, comment="マイルストーンならTrue")
    is_milestone_reached = Column('is_milestone_reached', Boolean, nullable=False, default=False, comment="マイルストーン到達済み")
    is_canceled = Column('is_canceled', Boolean, nullable=False, default=False, comment="アクティビティがキャンセル済みならTrue")
    cancel_reason = Column('cancel_reason', String(255), nullable=True, comment="キャンセル理由")
    canceled_by = Column('canceled_by', String(36), nullable=True, comment="キャンセル操作ユーザーUUID")
    is_terminal = Column('is_terminal', Boolean, nullable=False, default=False, comment="終了ノードならTrue")
    is_discriminator_loser = Column('is_discriminator_loser', Boolean, nullable=False, default=False, comment="Discriminator合流時に負けた経路ならTrue")
    is_deferred_choice_winner = Column('is_deferred_choice_winner', Boolean, nullable=False, default=False, comment="Deferred Choiceで勝者ならTrue")
    is_deferred_choice_loser = Column('is_deferred_choice_loser', Boolean, nullable=False, default=False, comment="Deferred Choiceで敗者ならTrue")
    trigger_type = Column('trigger_type', String(50), nullable=True, comment="トリガー種別（イベント名や条件式）")
    is_triggered = Column('is_triggered', Boolean, nullable=False, default=False, comment="トリガー発生済み")
    triggered_at = Column('triggered_at', TIMESTAMP, nullable=True, comment="トリガー発生日時")
    reaching_date = Column('reaching_date', TIMESTAMP, nullable=True, comment="到達日")
    process_date = Column('process_date', TIMESTAMP, nullable=True, comment="処理日")
    activity_status = Column('activity_status', EnumType(enum_class=ActivityStatus), nullable=True, comment="承認者状態")
    approverl_comment = Column('approverl_comment', String(255), nullable=True, comment="承認者のコメント")
    is_completed = Column('is_completed', Boolean, nullable=False, default=False, comment="アクティビティの完了状態")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_t_activity_objecttenant_uuid_application_number', tenant_uuid, application_number),
        Index('ix_t_activity_objecttenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, application_number, route_type, route_number, approverl_tenant_uuid, approverl_group_code, approverl_user_uuid),
    )

class Appended(Base):
    """
    　添付オブジェクト
    """

    __tablename__ = 't_appended'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="申請番号")
    route_type = Column('route_type', Integer, nullable=False, comment="ルートタイプ")
    route_number = Column('route_number', Integer, nullable=False, comment="ルートナンバー")
    group_key = Column('group_key', String(20), nullable=True, comment="分岐グループ識別子")
    approverl_tenant_uuid = Column('approverl_tenant_uuid', String(36), nullable=True, comment="承認者のテナントUUID")
    approverl_group_code = Column('approverl_group_code', String(10), nullable=False, comment="承認者の部署コード")
    approverl_user_uuid = Column('approverl_user_uuid', String(36), nullable=False, comment="承認者のユーザーUUID")
    append_title = Column('append_title', String(255), nullable=False, comment="添付ファイルの説明")
    append_path = Column('append_path', String(255), nullable=False, comment="添付ファイルのパス")
    append_date = Column('append_date', TIMESTAMP, nullable=False, comment="添付ファイルの登録日")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_t_appendedtenant_uuid_application_number', tenant_uuid, application_number),
        Index('ix_t_appendedtenant_uuid', tenant_uuid),
        UniqueConstraint(tenant_uuid, application_number, route_type, route_number),
    )

class RouteHistory(Base):
    """
    　申請書履歴オブジェクト
    """

    __tablename__ = 't_route_history'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    group_key = Column('group_key', String(20), nullable=True, comment="分岐グループ識別子")
    company_name = Column('company_name', String(50), nullable=False, comment="会社名")
    application_number = Column('application_number', Integer, nullable=False, comment="申請番号")
    re_application_number = Column('re_application_number', Integer, nullable=True, comment="旧申請番号")
    application_form_code = Column('application_form_code', String(10), nullable=False, comment="申請書コード")
    application_form_name = Column('application_form_name', String(30), nullable=False, comment="申請書名")
    target_tenant_uuid = Column('target_tenant_uuid', String(36), nullable=False, comment="対象者のテナントUUID")
    target_company_name = Column('target_company_name', String(50), nullable=False, comment="対象者の会社名")
    target_group_code = Column('target_group_code', String(10), nullable=False, comment="対象者の部署コード")
    target_group_name = Column('target_group_name', String(50), nullable=False, comment="対象者の部署名")
    target_user_uuid = Column('target_user_uuid', String(36), nullable=False, comment="対象者のユーザーUUID")
    target_employee_name = Column('target_employee_name', String(30), nullable=False, comment="対象者の氏名")
    applicant_tenant_uuid = Column('applicant_tenant_uuid', String(36), nullable=False, comment="申請者のテナントUUID")
    applicant_company_name = Column('applicant_company_name', String(50), nullable=False, comment="申請者の会社名")
    applicant_group_code = Column('applicant_group_code', String(10), nullable=False, comment="申請者の部署コード")
    applicant_group_name = Column('applicant_group_name', String(50), nullable=False, comment="申請者の部署名")
    applicant_user_uuid = Column('applicant_user_uuid', String(36), nullable=False, comment="申請者のユーザーUUID")
    applicant_employee_name = Column('applicant_employee_name', String(30), nullable=False, comment="申請者の氏名")
    apply_date = Column('apply_date', TIMESTAMP, nullable=False, comment="申請日")
    approval_date = Column('approval_date', TIMESTAMP, nullable=True, comment="承認日")
    application_status = Column('application_status', EnumType(enum_class=ApplicationStatus), nullable=False, comment="申請書状態")
    applicant_status = Column('applicant_status', EnumType(enum_class=ApplicantStatus), nullable=True, comment="申請者状態")
    route_type = Column('route_type', Integer, nullable=True, comment="ルートタイプ")
    route_number = Column('route_number', Integer, nullable=True, comment="ルートナンバー")
    approverl_tenant_uuid = Column('approverl_tenant_uuid', String(36), nullable=True, comment="承認者のテナントUUID")
    approverl_company_name = Column('approverl_company_name', String(50), nullable=True, comment="承認者の会社名")
    approverl_role_code = Column('approverl_role_code', String(30), nullable=True, comment="承認者の利用権限コード")
    approverl_role_name = Column('approverl_role_name', String(30), nullable=True, comment="承認者の利用権限名")
    approverl_group_code = Column('approverl_group_code', String(10), nullable=True, comment="承認者の部署コード")
    approverl_group_name = Column('approverl_group_name', String(50), nullable=True, comment="承認者の部署名")
    approverl_user_uuid = Column('approverl_user_uuid', String(36), nullable=True, comment="承認者のユーザーUUID")
    approverl_employee_name = Column('approverl_employee_name', String(30), nullable=True, comment="承認者氏名")
    deputy_approverl_tenant_uuid = Column('deputy_approverl_tenant_uuid', String(36), nullable=True, comment="代理承認者のテナントUUID")
    deputy_approverl_company_name = Column('deputy_approverl_company_name', String(50), nullable=True, comment="代理承認者の会社名")
    deputy_approverl_group_code = Column('deputy_approverl_group_code', String(10), nullable=True, comment="代理承認者の部署コード")
    deputy_approverl_group_name = Column('deputy_approverl_group_name', String(50), nullable=True, comment="代理承認者の部署名")
    deputy_approverl_user_uuid = Column('deputy_approverl_user_uuid', String(36), nullable=True, comment="代理承認者のユーザーUUID")
    deputy_approverl_employee_name = Column('deputy_approverl_employee_name', String(30), nullable=True, comment="代理承認者氏名")
    deputy_contents = Column('deputy_contents', String(255), nullable=True, comment="依頼理由")
    function = Column('function', EnumType(enum_class=ApprovalFunction), nullable=True, comment="承認画面の機能")
    reaching_date = Column('reaching_date', TIMESTAMP, nullable=True, comment="到達日")
    process_date = Column('process_date', TIMESTAMP, nullable=True, comment="処理日")
    activity_status = Column('activity_status', EnumType(enum_class=ActivityStatus), nullable=True, comment="承認者状態")
    approverl_comment = Column('approverl_comment', String(255), nullable=True, comment="承認者のコメント")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }



class ActivityTransit(Base):
    """
    　アクティビティ遷移定義（AND/OR/条件分岐）
    """

    __tablename__ = 't_activity_transit'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="対象申請番号")
    from_route_type = Column('from_route_type', Integer, nullable=False, comment="遷移元ルートタイプ")
    from_route_number = Column('from_route_number', Integer, nullable=False, comment="遷移元ルートナンバー")
    to_route_type = Column('to_route_type', Integer, nullable=False, comment="遷移先ルートタイプ")
    to_route_number = Column('to_route_number', Integer, nullable=False, comment="遷移先ルートナンバー")
    transition_type = Column('transition_type', EnumType(enum_class=TransitionType), nullable=False, comment="遷移タイプ（AND/OR/CONDITION）")
    group_key = Column('group_key', String(20), nullable=True, comment="分岐グループキー")
    condition_expression = Column('condition_expression', String(255), nullable=True, comment="条件式（JSONやDSL）")
    approval_condition_type = Column('approval_condition_type', EnumType(enum_class=ApprovalConditionType), nullable=False, default=ApprovalConditionType.ALL, comment="承認完了条件の種別（ALL=全員, MAJORITY=過半数, ANY=誰か1人）")
    approval_threshold = Column('approval_threshold', Integer, nullable=True, comment="任意人数承認で可とする場合の閾値（approval_condition_type='THRESHOLD'時）")
    sort_number = Column('sort_number', Integer, nullable=True, comment="並び順")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }



class ApplicationComment(Base):
    """
    　申請チャット／コメント情報（掲示板形式、スレッド対応）
    """

    __tablename__ = 't_application_comment'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="紐づく申請番号")
    parent_comment_id = Column('parent_comment_id', Integer, nullable=True, comment="親コメントID（返信先がある場合）")
    route_type = Column('route_type', Integer, nullable=True, comment="書き込んだ人のルートタイプ（明細とリンク）")
    route_number = Column('route_number', Integer, nullable=True, comment="書き込んだ人のルートナンバー（明細とリンク）")
    poster_user_uuid = Column('poster_user_uuid', String(36), nullable=False, comment="投稿者のユーザーUUID")
    poster_group_code = Column('poster_group_code', String(10), nullable=False, comment="投稿者の部署コード")
    comment_text = Column('comment_text', String(2000), nullable=False, comment="コメント内容")
    posted_at = Column('posted_at', TIMESTAMP, nullable=False, default=datetime.now, comment="投稿日時")
    is_deleted = Column('is_deleted', Boolean, nullable=False, default=False, comment="ソフト削除フラグ")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)



    __mapper_args__ = {
        'version_id_col': update_count
    }

    __table_args__ = (
        Index('ix_t_application_commenttenant_uuid_application_number', tenant_uuid, application_number),
        Index('ix_t_application_commentparent_comment_id', parent_comment_id),
        Index('ix_t_application_commentposter_user_uuid', poster_user_uuid),
    )

class ApplicationCommentReadStatus(Base):
    """
    　申請チャットコメント既読ステータス
    """

    __tablename__ = 't_application_comment_read_status'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    comment_id = Column('comment_id', Integer, nullable=False, comment="コメントID（t_application_comment.idへの外部キー）")
    user_uuid = Column('user_uuid', String(36), nullable=False, comment="既読したユーザーのUUID")
    read_at = Column('read_at', TIMESTAMP, nullable=True, comment="既読日時")






class ApplicationCommentAttachment(Base):
    """
    　申請チャットコメントの添付ファイル情報
    """

    __tablename__ = 't_application_comment_attachment'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    comment_id = Column('comment_id', Integer, nullable=False, comment="対象のコメントID（t_application_comment.idへの外部キー）")
    file_name = Column('file_name', String(255), nullable=False, comment="添付ファイル名")
    file_path = Column('file_path', String(255), nullable=False, comment="添付ファイルパス")






class WorkflowTrigger(Base):
    """
    　サブプロセス自動起動定義（申請間連携トリガー）
    """

    __tablename__ = 't_workflow_trigger'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    trigger_form_code = Column('trigger_form_code', String(10), nullable=False, comment="トリガー元の申請書コード（例：出張申請）")
    trigger_activity_code = Column('trigger_activity_code', Integer, nullable=True, comment="トリガー元のアクティビティコード（例：課長承認）※NULLなら完了時")
    target_form_code = Column('target_form_code', String(10), nullable=False, comment="起動する申請書コード（例：出張報告申請）")
    inherit_mode = Column('inherit_mode', EnumType(enum_class=InheritMode), nullable=False, comment="引き継ぎモード（USER_ONLY / GROUP / FULL）")
    trigger_condition = Column('trigger_condition', String(255), nullable=True, comment="条件式（DSL or JSON）で実行条件を制限可能")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_t_workflow_triggertenant_uuid_trigger_form_code', tenant_uuid, trigger_form_code),
        UniqueConstraint(tenant_uuid, trigger_form_code, trigger_activity_code, target_form_code),
    )

class DynamicRouteNode(Base):
    """
    　動的承認ルート定義（申請単位で承認者を指定）
    """

    __tablename__ = 't_dynamic_route_node'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="紐づく申請番号")
    route_type = Column('route_type', Integer, nullable=False, comment="紐づくルートタイプ")
    route_number = Column('route_number', Integer, nullable=False, comment="紐づくルートナンバー")
    approverl_user_uuid = Column('approverl_user_uuid', String(36), nullable=False, comment="承認者ユーザーUUID（動的に指定）")
    approverl_group_code = Column('approverl_group_code', String(10), nullable=True, comment="承認者部署コード（オプション）")
    function = Column('function', EnumType(enum_class=ApprovalFunction), nullable=False, comment="承認機能タイプ")
    comment = Column('comment', String(255), nullable=True, comment="動的指定の理由や説明")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_t_dynamic_route_nodetenant_uuid_application_number_route_type_route_number', tenant_uuid, application_number, route_type, route_number),
        Index('ix_t_dynamic_route_nodeapproverl_user_uuid', approverl_user_uuid),
        UniqueConstraint(tenant_uuid, application_number, route_type, route_number),
    )

class ReworkRoute(Base):
    """
    　差し戻しルート定義（特定アクティビティから戻るルートを明示的に定義）
    """

    __tablename__ = 't_rework_route'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_form_code = Column('application_form_code', String(10), nullable=False, comment="対象の申請書コード")
    from_route_type = Column('from_route_type', Integer, nullable=False, comment="差し戻し元のルートタイプ")
    from_route_number = Column('from_route_number', Integer, nullable=False, comment="差し戻し元のルートナンバー")
    to_route_type = Column('to_route_type', Integer, nullable=False, comment="差し戻し先のルートタイプ")
    to_route_number = Column('to_route_number', Integer, nullable=False, comment="差し戻し先のルートナンバー")
    condition_expression = Column('condition_expression', String(255), nullable=True, comment="差し戻し条件式（DSL/JSONLogicなどで柔軟に指定可能）")
    comment = Column('comment', String(255), nullable=True, comment="差し戻しの説明・備考など")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_t_rework_routetenant_uuid_application_form_code', tenant_uuid, application_form_code),
        Index('ix_t_rework_routetenant_uuid_from_route_type_from_route_number', tenant_uuid, from_route_type, from_route_number),
        UniqueConstraint(tenant_uuid, application_form_code, from_route_type, from_route_number, to_route_type, to_route_number),
    )

class FieldVisibility(Base):
    """
    　フィールド可視性定義（アクティビティ単位でフォーム項目の表示制御を行う）
    """

    __tablename__ = 't_field_visibility'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_form_code = Column('application_form_code', String(10), nullable=False, comment="対象の申請書コード")
    activity_code = Column('activity_code', Integer, nullable=False, comment="対象のアクティビティコード（m_individual_activity等と一致）")
    field_name = Column('field_name', String(50), nullable=False, comment="対象フィールド名（テーブルカラムや画面項目名）")
    visibility = Column('visibility', EnumType(enum_class=FieldVisibilityType), nullable=False, comment="表示制御種別（VISIBLE, READONLY, HIDDEN）")
    editable_by_applicant = Column('editable_by_applicant', Boolean, nullable=False, default=False, comment="申請者が編集可能かどうか")
    editable_by_approver = Column('editable_by_approver', Boolean, nullable=False, default=False, comment="承認者が編集可能かどうか")
    comment = Column('comment', String(255), nullable=True, comment="補足・用途メモ")
    label_key = Column('label_key', String(100), nullable=True, comment="ラベルキー（m_message等と連携して多言語表示に使用）")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_t_field_visibilitytenant_uuid_application_form_code_activity_code', tenant_uuid, application_form_code, activity_code),
        Index('ix_t_field_visibilitytenant_uuid_field_name', tenant_uuid, field_name),
        UniqueConstraint(tenant_uuid, application_form_code, activity_code, field_name),
    )

class ApplicationSnapshot(Base):
    """
    　申請スナップショット履歴（ロールバック対応用の状態保存）
    """

    __tablename__ = 't_application_snapshot'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_number = Column('application_number', Integer, nullable=False, comment="対象申請番号")
    version_number = Column('version_number', Integer, nullable=False, comment="スナップショットのバージョン番号（連番）")
    snapshot_data = Column('snapshot_data', String(255), nullable=False, comment="申請全体の状態を保存したJSON（ApplicationObject＋ActivityObject群など）")
    snapshot_reason = Column('snapshot_reason', String(255), nullable=True, comment="スナップショット取得理由（手動 or 自動など）")
    revert_to_version = Column('revert_to_version', Integer, nullable=True, comment="ロールバック時に戻した先のバージョン（NULL以外なら復元記録）")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_t_application_snapshottenant_uuid_application_number_version_number', tenant_uuid, application_number, version_number),
        UniqueConstraint(tenant_uuid, application_number, version_number),
    )

class ApprovalPolicy(Base):
    """
    　承認ポリシー定義（金額・部署などの条件によってルート切替）
    """

    __tablename__ = 't_approval_policy'
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment="サロゲートキー")
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_form_code = Column('application_form_code', String(10), nullable=False, comment="対象の申請書コード")
    policy_expression = Column('policy_expression', String(1000), nullable=False, comment="条件式（DSL / JSONLogicで申請内容に基づく分岐条件を記述）")
    route_override_code = Column('route_override_code', String(10), nullable=False, comment="条件を満たしたときに使うルートコード（個別または共通ルート）")
    route_type = Column('route_type', EnumType(enum_class=RouteType), nullable=False, comment="ルートの種別（INDIVIDUAL / COMMON）")
    priority = Column('priority', Integer, nullable=False, default=100, comment="評価順（小さいほど優先）")
    is_active = Column('is_active', Boolean, nullable=False, default=True, comment="有効フラグ")
    comment = Column('comment', String(255), nullable=True, comment="補足・条件の説明など")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_t_approval_policytenant_uuid_application_form_code_priority', tenant_uuid, application_form_code, priority),
        UniqueConstraint(tenant_uuid, application_form_code, policy_expression),
    )

class Message(Base):
    """
    　多言語メッセージマスタ（UI文言・ラベル等を管理）
    """

    __tablename__ = 'm_message'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    language_code = Column('language_code', String(5), nullable=False, comment="言語コード（例：ja-JP, en-US）")
    message_key = Column('message_key', String(100), nullable=False, comment="ラベル・エラー文等のキー")
    message_text = Column('message_text', String(255), nullable=False, comment="表示メッセージ")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        UniqueConstraint(language_code, message_key),
    )

class WorkflowGraphView(Base):
    """
    　ワークフロー構造可視化用ビュー（Mermaid等の構成図出力元データ）
    """

    __tablename__ = 't_workflow_graph_view'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    tenant_uuid = Column('tenant_uuid', String(36), nullable=False, comment="テナントUUID")
    application_form_code = Column('application_form_code', String(10), nullable=False, comment="申請書コード")
    route_type = Column('route_type', Integer, nullable=False, comment="ルートタイプ（1:個別, 2:共通）")
    from_activity_code = Column('from_activity_code', Integer, nullable=False, comment="遷移元アクティビティコード")
    from_function = Column('from_function', EnumType(enum_class=ApprovalFunction), nullable=False, comment="遷移元の承認機能タイプ")
    to_activity_code = Column('to_activity_code', Integer, nullable=False, comment="遷移先アクティビティコード")
    to_function = Column('to_function', EnumType(enum_class=ApprovalFunction), nullable=False, comment="遷移先の承認機能タイプ")
    transition_type = Column('transition_type', EnumType(enum_class=TransitionType), nullable=False, comment="遷移種別（AND / OR / CONDITION）")
    condition_expression = Column('condition_expression', String(255), nullable=True, comment="条件式（JSONLogic/DSL等）")
    group_key = Column('group_key', String(20), nullable=True, comment="分岐グループキー")
    sort_number = Column('sort_number', Integer, nullable=True, comment="並び順（図描画用）")
    create_date = Column('create_date', TIMESTAMP, nullable=False, default=datetime.now)
    create_user_uuid = Column('create_user_uuid', String(36), nullable=False)
    update_date = Column('update_date', TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    update_user_uuid = Column('update_user_uuid', String(36), nullable=False)
    update_count = Column('update_count', Integer, nullable=False)




    __table_args__ = (
        Index('ix_t_workflow_graph_viewtenant_uuid_application_form_code', tenant_uuid, application_form_code),
    )