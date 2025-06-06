from enum import IntEnum


class AutoApproverlFlag(IntEnum):
    """
    自動承認フラグ
    AUTOMATIC_APPROVAL: 自動承認
    MANUAL_APPROVAL: 手動承認
    """
    AUTOMATIC_APPROVAL = 1  # 自動承認
    MANUAL_APPROVAL = 2     # 手動承認


class PullingFlag(IntEnum):
    """
    引き戻し区分フラグ（用途に合わせて値を修正してください）
    """
    A = 1  # 区分A
    B = 2  # 区分B


class WithdrawalFlag(IntEnum):
    """
    取り下げ区分フラグ
    ENABLED: 取り下げ可能
    DISABLED: 取り下げ不可
    """
    ENABLED = 1   # 取り下げ可能
    DISABLED = 2  # 取り下げ不可


class RouteFlag(IntEnum):
    """
    直接部門・間接部門の区分
    DIRECT: 直接部門
    INDIRECT: 間接部門
    """
    DIRECT = 1    # 直接部門
    INDIRECT = 2  # 間接部門


class ApplicationStatus(IntEnum):
    """
    申請書の状態
    DRAFT: 下書き
    SUBMITTED: 提出済み
    APPROVED: 承認済み
    REJECTED: 否認
    """
    DRAFT = 1      # 下書き
    SUBMITTED = 2  # 提出済み
    APPROVED = 3   # 承認済み
    REJECTED = 4   # 否認


class ApprovalFunction(IntEnum):
    """
    承認画面での機能種類
    EXAMINATION: 審査
    AUTHORIZER_AUTOMATIC_APPROVAL: 自動承認
    FUNCTION_CONFIRMATION: 確認
    AUTHORIZER_FORCED_APPROVAL: 強制承認
    """
    EXAMINATION = 1                    # 審査
    AUTHORIZER_AUTOMATIC_APPROVAL = 2  # 自動承認
    FUNCTION_CONFIRMATION = 3          # 確認
    AUTHORIZER_FORCED_APPROVAL = 4     # 強制承認


class ActivityStatus(IntEnum):
    """
    承認アクティビティの状態
    IN_PROGRESS: 進行中
    COMPLETED: 完了
    CANCELED: キャンセル
    """
    IN_PROGRESS = 1  # 進行中
    COMPLETED = 2    # 完了
    CANCELED = 3     # キャンセル


class ApplicantStatus(IntEnum):
    """
    申請者状態
    NEW: 新規
    SENT: 送信済み
    RECEIVED: 受領済み
    CANCELED: 取り消し
    """
    NEW = 1       # 新規
    SENT = 2      # 送信済み
    RECEIVED = 3  # 受領済み
    CANCELED = 4  # 取り消し


class TransitionType(IntEnum):
    """
    アクティビティ遷移タイプ
    AND: AND条件
    OR: OR条件
    CONDITION: 条件分岐
    """
    AND = 1        # AND条件
    OR = 2         # OR条件
    CONDITION = 3  # 条件分岐


class ApprovalConditionType(IntEnum):
    """
    承認完了条件の種類
    ALL: 全員
    MAJORITY: 過半数
    ANY: 誰か1人
    THRESHOLD: 指定人数以上
    """
    ALL = 1        # 全員
    MAJORITY = 2   # 過半数
    ANY = 3        # 誰か1人
    THRESHOLD = 4  # 指定人数以上
