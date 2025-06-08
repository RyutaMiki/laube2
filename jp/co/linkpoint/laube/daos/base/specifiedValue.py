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

# --- 必要に応じて追加可能 ---
