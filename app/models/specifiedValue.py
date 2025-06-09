from enum import IntEnum

# --- 各種 Enum定義 ---


class AutoApproverlFlag(IntEnum):
    """自動承認フラグ / Auto approval flag"""
    AUTOMATIC_APPROVAL = 1  # 自動承認 / Automatic
    MANUAL_APPROVAL = 2     # 手動承認 / Manual


class PullingFlag(IntEnum):
    """引き戻し区分フラグ / Pulling back category"""
    A = 1  # 区分A / Category A
    B = 2  # 区分B / Category B


class WithdrawalFlag(IntEnum):
    """取り下げ区分フラグ / Withdrawal flag"""
    ENABLED = 1   # 取り下げ可能 / Enabled
    DISABLED = 2  # 取り下げ不可 / Disabled


class RouteFlag(IntEnum):
    """直接/間接部門フラグ / Route flag"""
    DIRECT = 1    # 直接部門 / Direct
    INDIRECT = 2  # 間接部門 / Indirect


class ApplicationStatus(IntEnum):
    """申請書状態 / Application Status"""
    DRAFT = 1      # 下書き / Draft
    SUBMITTED = 2  # 提出済み / Submitted
    APPROVED = 3   # 承認済み / Approved
    REJECTED = 4   # 否認 / Rejected


class ApprovalFunction(IntEnum):
    """承認機能区分 / Approval Function"""
    EXAMINATION = 1                    # 審査 / Examination
    AUTHORIZER_AUTOMATIC_APPROVAL = 2  # 自動承認 / Automatic approval
    FUNCTION_CONFIRMATION = 3          # 確認 / Confirmation
    AUTHORIZER_FORCED_APPROVAL = 4     # 強制承認 / Forced approval


class ActivityStatus(IntEnum):
    """アクティビティ状態 / Activity Status"""
    IN_PROGRESS = 1  # 進行中 / In progress
    COMPLETED = 2    # 完了 / Completed
    CANCELED = 3     # キャンセル / Canceled


class ApplicantStatus(IntEnum):
    """申請者状態 / Applicant Status"""
    NEW = 1       # 新規 / New
    SENT = 2      # 送信済み / Sent
    RECEIVED = 3  # 受領済み / Received
    CANCELED = 4  # 取り消し / Canceled


class TransitionType(IntEnum):
    """アクティビティ遷移タイプ / Transition Type"""
    AND = 1        # AND条件 / AND
    OR = 2         # OR条件 / OR
    CONDITION = 3  # 条件分岐 / Condition


class ApprovalConditionType(IntEnum):
    """承認条件タイプ / Approval Condition Type"""
    ALL = 1        # 全員 / All
    MAJORITY = 2   # 過半数 / Majority
    ANY = 3        # 誰か1人 / Any
    THRESHOLD = 4  # 指定人数以上 / Threshold


class StatusFlag(IntEnum):
    """状態フラグ / Status Flag"""
    ENABLED = 1   # 有効 / Enabled
    DISABLED = 2  # 無効 / Disabled


class PermissionRange(IntEnum):
    """利用権限範囲 / Permission Range"""
    ALL = 1            # すべて / All
    GROUP_ONLY = 2     # 部署のみ / Group Only
    INDIVIDUAL = 3     # 個人のみ / Individual Only


class DefaultGroupFlg(IntEnum):
    """
    Enum:デフォルト部署フラグ
    ON デフォルト部署
    OFF その他
    """
    ON = 1
    OFF = 2


class Range(IntEnum):
    """
    Enum:利用権限範囲
    PERSONAL 個人
    ALL 全員
    """
    PERSONAL = 1
    ALL = 2


class InheritMode(IntEnum):
    """
    Enum:利用権限範囲
    USER_ONLY ユーザーUUIDのみ引き継ぎ
    GROUP 所属部署・ユーザー情報を引き継ぎ
    FULL 申請内容まるごと（JSONで渡す）引き継ぎ
    """
    USER_ONLY = 1
    GROUP = 2
    FULL = 3


class EscalationAction(IntEnum):
    """タイムアウト時の自動処理アクション / Escalation Action"""
    ESCALATE = 1   # 上位者へエスカレーション / Escalate to superior
    SKIP = 2       # スキップして次へ進む / Skip to next
    APPROVE = 3    # 自動で承認 / Auto approve
    RETURN = 4     # 差し戻し（前段階または申請者へ）/ Return to previous or applicant


class ConditionExpressionType(IntEnum):
    """条件式の評価エンジン種別 / Condition Expression Type"""
    DSL = 1          # 独自の簡易DSL（例：applicant_user_uuid == 'abc'）
    JSONLOGIC = 2    # JSONLogic形式
    JMESPATH = 3     # JMESPath形式


class FieldVisibilityType(IntEnum):
    """フィールドの表示制御種別 / Field Visibility Type"""
    VISIBLE = 1    # 表示・編集可能
    READONLY = 2   # 表示のみ
    HIDDEN = 3     # 非表示


class RouteType(IntEnum):
    """ルート種別 / Route Type"""
    INDIVIDUAL = 1  # 直接部門ルート
    COMMON = 2      # 間接部門ルート


class SkipMode(IntEnum):
    """条件未成立時の制御モード / Skip Mode"""
    SKIP = 1     # 条件が満たされない場合スキップする
    BLOCK = 2    # 条件が満たされない場合処理を中断（エラー）
    WARN = 3     # 条件が満たされない場合警告を出して進行

# --- 必要に応じて追加可能 ---
