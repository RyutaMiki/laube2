from enum import IntEnum

class TransitionType(IntEnum):
    AND = 1
    OR = 2
    CONDITION = 3

class PrincipalType(IntEnum):
    ROLE = 1
    USER = 2
    GROUP = 3


class ResourceType(IntEnum):
    SCREEN = 1
    API = 2
    MENU = 3


class ActionType(IntEnum):
    ENTRY = 1
    UPDATE = 2
    DELETE = 3
    PRINT = 4
    SEARCH = 5
    UPLOAD = 6
    DOWNLOAD = 7
    PREVIEW = 8
    CALL = 9


class EffectType(IntEnum):
    ALLOW = 1
    DENY = 2


class Availability(IntEnum):
    AVAILABLE = 1
    UNUSABLE = 2


class WorkingSystemType(IntEnum):
    NORMAL = 1
    FLEX = 2
    TRANSFORMATION = 3


class FlexibleLaborType(IntEnum):
    ONE_MONTH = 1
    ONE_YEAR = 2


class JobBeforeStartTime(IntEnum):
    INCLUDE = 1
    EXCLUDE = 2


"""
Enum:打刻区分
JOB_START            出勤打刻
JOB_FINISH            退勤打刻
BREAKTIME_START        休憩開始打刻
BREAKTIME_FINISH    休憩終了打刻
"""




"""
Enum:打刻方法
CORPUS コーパスからの移行
SMART_PHONE スマホ打刻
PC パソコン打刻
FELICA フェリカ打刻
QRCODE QRバーコード打刻
TABLET タブレット打刻
VEIN_AUTHENTICATION 静脈認証打刻
FINGERPRINT_AUTHENTICATION 指紋認証打刻
FACE_AUTHENTICATION 顔認証打刻
IMPRINT_CORRECTION 打刻補正
KRONOS 自動登録
ALEXA Alexa打刻
INPUT_ATTENDANCE_RECORD 出勤簿手入力
"""


class EntryFlg(IntEnum):
    CORPUS = 1
    SMART_PHONE = 2
    PC = 3
    FELICA = 4
    QRCODE = 5
    TABLET = 6
    VEIN_AUTHENTICATION = 7
    FINGERPRINT_AUTHENTICATION = 8
    FACE_AUTHENTICATION = 9
    IMPRINT_CORRECTION = 10
    KRONOS = 11
    ALEXA = 12
    INPUT_ATTENDANCE_RECORD = 13

    @property
    def label(self) -> str:
        return {
            EntryFlg.CORPUS: "コーパスからの移行",
            EntryFlg.SMART_PHONE: "スマホ打刻",
            EntryFlg.PC: "パソコン打刻",
            EntryFlg.FELICA: "フェリカ打刻",
            EntryFlg.QRCODE: "QRバーコード打刻",
            EntryFlg.TABLET: "タブレット打刻",
            EntryFlg.VEIN_AUTHENTICATION: "静脈認証打刻",
            EntryFlg.FINGERPRINT_AUTHENTICATION: "指紋認証打刻",
            EntryFlg.FACE_AUTHENTICATION: "顔認証打刻",
            EntryFlg.IMPRINT_CORRECTION: "打刻補正",
            EntryFlg.KRONOS: "自動登録",
            EntryFlg.ALEXA: "Alexa打刻",
            EntryFlg.INPUT_ATTENDANCE_RECORD: "出勤簿手入力",
        }[self]


class StampingType(IntEnum):
    JOB_START = 1
    JOB_FINISH = 2
    BREAKTIME_START = 3
    BREAKTIME_FINISH = 4

    @property
    def label(self) -> str:
        return {
            StampingType.JOB_START: "出勤打刻",
            StampingType.JOB_FINISH: "退勤打刻",
            StampingType.BREAKTIME_START: "休憩開始打刻",
            StampingType.BREAKTIME_FINISH: "休憩終了打刻",
        }[self]


class ApprovalConditionType(IntEnum):
    ALL = 1  # 全員
    MAJORITY = 2  # 過半数
    ANY = 3  # 誰か1人
    THRESHOLD = 4  # 指定人数以上


"""
Enum:反映フラグ
WAIT 作成中
REFLECTED 反映済
NON_REFLECTED 未反映
ERROR_DUPLICATE 出勤中に出勤打刻エラー
"""


class ReflectionFlg(IntEnum):
    WAIT = 1
    REFLECTED = 2
    NON_REFLECTED = 3
    ERROR_DUPLICATE = 4

    @property
    def label(self) -> str:
        return {
            ReflectionFlg.WAIT: "作成中",
            ReflectionFlg.REFLECTED: "反映済",
            ReflectionFlg.NON_REFLECTED: "未反映",
            ReflectionFlg.ERROR_DUPLICATE: "出勤中に出勤打刻エラー",
        }[self]


"""
Enum:自動承認フラグ
AUTOMATIC_APPROVAL 自動承認
MANUAL_APPROVAL 手動承認
"""


class AutoApproverlFlag(IntEnum):
    AUTOMATIC_APPROVAL = 1
    MANUAL_APPROVAL = 2



"""
Enum:所定労働日区分
ON 　所定労働日扱い
OFF　所定労働日扱いしない
"""


class LaborDayClassification(IntEnum):
    ON = 1
    OFF = 2

"""
Enum:出勤日扱い区分
ON 　出勤日扱いする
OFF　出勤日扱いしない
"""


class AttendanceDateClassification(IntEnum):
    ON = 1
    OFF = 2


"""
Enum:賃金支給区分
ON 　賃金支給する
OFF　賃金支給しない
"""


class WageClassification(IntEnum):
    ON = 1
    OFF = 2

"""
Enum:事由マスタ　出勤簿利用可否
AVAILABLE 利用可能
UNAVAILABLE 利用不可
OUT 利用不可[変更不可]
"""


class TimecardAvailableFlg(IntEnum):
    AVAILABLE = 1
    UNAVAILABLE = 2
    OUT = 9


class NonStampFlg(IntEnum):
    AVAILABLE = 1
    UNAVAILABLE = 2


"""
Enum:色
BLACK 黒色
BLUE 青色
RED 赤色
GREEN 緑色
"""


class Color(IntEnum):
    BLACK = 1
    BLUE = 2
    RED = 3
    GREEN = 4


"""
Enum:申請対象フラグ
ON 対象
OFF 対象外
OUT 対象外[利用不可]
"""


class WorkflowFlg(IntEnum):
    ON = 1
    OFF = 2
    OUT = 9


"""
Enum:システム画面フラグ
ON システム画面
OFF システム画面以外
"""


class SystemScreenFlg(IntEnum):
    ON = 1
    OFF = 2

    @property
    def label(self) -> str:
        return {
            SystemScreenFlg.ON: "システム画面",
            SystemScreenFlg.OFF: "システム画面以外",
        }[self]


"""
Enum:画面種別
MAIN メイン画面
POPUP ポップアップ画面
DASH_BOARD ダッシュボード
"""


class ScreenType(IntEnum):
    MAIN = 1
    POPUP = 2
    DASH_BOARD = 3

    @property
    def label(self) -> str:
        return {
            ScreenType.MAIN: "メイン画面",
            ScreenType.POPUP: "ポップアップ画面",
            ScreenType.DASH_BOARD: "ダッシュボード",
        }[self]


"""
Enum:システム管理会社フラグ
ON システム管理会社
OFF 一般会社
"""


class SystemCompanyFlg(IntEnum):
    ON = 1
    OFF = 2

    @property
    def label(self) -> str:
        return {
            SystemCompanyFlg.ON: "システム管理会社",
            SystemCompanyFlg.OFF: "一般会社",
        }[self]


"""
Enum:承認画面の機能
EXAMINATION 審査
AUTHORIZER_AUTOMATIC_APPROVAL 自動承認
FUNCTION_CONFIRMATION 確認
AUTHORIZER_FORCED_APPROVAL 強制承認
"""


class ApprovalFunction(IntEnum):
    EXAMINATION = 1
    AUTHORIZER_AUTOMATIC_APPROVAL = 2
    FUNCTION_CONFIRMATION = 3
    AUTHORIZER_FORCED_APPROVAL = 4


"""
Enum:権限の譲渡フラグ
AVAILABLE 可能です
UNUSABLE 出来ません
"""


class Permission(IntEnum):
    AVAILABLE = 1
    UNUSABLE = 2


class PullingFlag(IntEnum):
    # 何か値
    A = 1
    B = 2


class WithdrawalFlag(IntEnum):
    ENABLED = 1
    DISABLED = 2


class RouteFlag(IntEnum):
    DIRECT = 1
    INDIRECT = 2


class ApplicationStatus(IntEnum):
    DRAFT = 1
    SUBMITTED = 2
    APPROVED = 3
    REJECTED = 4


class ActivityStatus(IntEnum):
    # 適宜、本来の値を定義
    IN_PROGRESS = 1
    COMPLETED = 2
    CANCELED = 3


class ApplicantStatus(IntEnum):
    NEW = 1
    SENT = 2
    RECEIVED = 3
    CANCELED = 4

