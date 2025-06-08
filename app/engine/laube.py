from datetime import date, datetime
from functools import wraps

from jp.co.linkpoint.artemis.util.utility import Utility
from jp.co.linkpoint.artemis.engine.engineUtility import EngineUtility
from jp.co.linkpoint.artemis.dao.base import ActivityObject
from jp.co.linkpoint.artemis.dao.base import ApplicationObject
from jp.co.linkpoint.artemis.dao.base import RouteHistory
from jp.co.linkpoint.artemis.dao.type.specifiedValue import EngineName, AutoApproverlFlag, ApprovalFunction, ApplicationStatus, ActivityStatus, RouteType, RouteFlag, ScreenMode, PullingFlag, ApplicantStatus
from jp.co.linkpoint.artemis.exception.laubeException import LaubeException
from jp.co.linkpoint.artemis.dao.activityObjectDao import ActivityObjectDao
from jp.co.linkpoint.artemis.dao.applicationClassificationDao import ApplicationClassificationDao
from jp.co.linkpoint.artemis.dao.applicationFormDao import ApplicationFormDao
from jp.co.linkpoint.artemis.dao.applicationFormRouteDao import ApplicationFormRouteDao
from jp.co.linkpoint.artemis.dto.applicationInfoDto import ApplicationInfoDto
from jp.co.linkpoint.artemis.dao.applicationObjectDao import ApplicationObjectDao
from jp.co.linkpoint.artemis.dto.approverlDataInfoDto import ApproverlDataInfoDto
from jp.co.linkpoint.artemis.dto.approverlDto import ApproverlDto
from jp.co.linkpoint.artemis.dao.bossDao import BossDao
from jp.co.linkpoint.artemis.dao.commonActivityDao import CommonActivityDao
from jp.co.linkpoint.artemis.dao.companyDao import CompanyDao
from jp.co.linkpoint.artemis.dao.deputyApprovelDao import DeputyApprovelDao
from jp.co.linkpoint.artemis.dao.employeeDao import EmployeeDao
from jp.co.linkpoint.artemis.dao.employeeAlertManagementDao import EmployeeAlertManagementDao
from jp.co.linkpoint.artemis.dao.employeeGroupDao import EmployeeGroupDao
from jp.co.linkpoint.artemis.dao.employeeGroupRoleDao import EmployeeGroupRoleDao
from jp.co.linkpoint.artemis.dao.employeeJobTitleDao import EmployeeJobTitleDao
from jp.co.linkpoint.artemis.dao.groupDao import GroupDao
from jp.co.linkpoint.artemis.dao.individualActivityDao import IndividualActivityDao
from jp.co.linkpoint.artemis.dao.roleDao import RoleDao
from jp.co.linkpoint.artemis.dao.routeHistoryDao import RouteHistoryDao
from jp.co.linkpoint.artemis.exception.artemisException import ArtemisException
from jp.co.linkpoint.artemis.util.send_grid_utility import SendGridUtility

##################################################################
# Copyright (c) 2016, Ryuta Miki All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##################################################################


class Laube():

    """
    初期処理を行います。
    Args:
        None
    Returns:
        None
    Raises:
        None
    """
    def __init__(self):

        self.utility = Utility()
        self.engineUtility = EngineUtility()

        # 審査者への承認待ちメール
        self.APPROVAL_PENDING_MAIL_SUBJECT = '{employee_name}({employee_code})様より承認依頼が届いています。'
        self.APPROVAL_PENDING_MAIL_BODY = '{employee_name}({employee_code})様より{application_form_name}の承認依頼が届いています。\n Artemis Collierにログインし[勤怠]メニュー内の[承認状況]にてご確認下さい。'

        # 確認者への確認待ちメール
        self.PENDING_VERIFICATION_MAIL_SUBJECT = '{employee_name}({employee_code})様より確認依頼が届いています。'
        self.PENDING_VERIFICATION_MAIL_BODY = '{employee_name}({employee_code})様より{application_form_name}の承認依頼が届いています。\n Artemis Collierにログインし[勤怠]メニュー内の[承認状況]にてご確認下さい。'

        # 申請者への最終承認済みメール
        self.APPROVED_MAIL_SUBJECT = '申請番号({application_number})が承認されました。'
        self.APPROVED_MAIL_BODY = '申請番号({application_number})の{application_form_name}が承認されました。\n Artemis Collierにログインし[勤怠]メニュー内の[申請状況]にてご確認下さい。'

        # 申請者への否認済みメール
        self.AUTHORIZER_DENIAL_MAIL_SUBJECT = '申請番号({application_number})が否認されました。'
        self.AUTHORIZER_DENIAL_MAIL_BODY = '申請番号({application_number})の{application_form_name}が否認されました。\n Artemis Collierにログインし[勤怠]メニュー内の[申請状況]にてご確認下さい。'

        # エラーメッセージ
        self.W001 = 'Laube-W001'  # エンジンが利用停止中の場合に発生します。

        self.E001 = 'Laube-E001'  # セッション情報がNoneの場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E002 = 'Laube-E002'  # 会社コード[対象者]がNoneの場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E003 = 'Laube-E003'  # 部署コード[対象者]がNoneの場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E004 = 'Laube-E004'  # 従業員番号[対象者]がNoneの場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E005 = 'Laube-E005'  # 申請書コードがNoneの場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E006 = 'Laube-E006'  # 申請書マスタが見つからなかった場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E007 = 'Laube-E007'  # 登録されていない個別ルートフラグが使われている場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E008 = 'Laube-E008'  # 会社コード[申請者]がNoneの場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E009 = 'Laube-E009'  # 部署コード[申請者]がNoneの場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E010 = 'Laube-E010'  # 従業員番号[申請者]がNoneの場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E011 = 'Laube-E011'  # 申請分類マスタが見つからなかった場合に発生します。このメソッドを呼び出したAPIを確認して下さい。
        self.E012 = 'Laube-E012'  # 承認ルート上に人事異動されている、または退職されている従業員が存在します。マスタ設定[ワークフロー]の承認経路画面でご確認下さい。

    def __health_check(f):
        """Laubeのヘルスチェックデコレーター"""

        @wraps(f)
        def wrapper(self, *args, **kwargs):
            """
            Laubeのヘルスチェックを実施します。

            Raises:
                LaubeException: [Laube-W001] エンジンが利用停止中の場合に発生します。
            """
            if self.engineUtility.is_mentenance(args[0], EngineName.Laube):
                raise LaubeException(self.W001)
            return f(self, *args, **kwargs)

        return wrapper

    def __get_database(self, session, company_code):
        """
        データベースより処理実行に必要なレコードを取得します。

        Args:
            session ([Session]): セッション情報
            company_code ([String]): 会社コード

        Raises:
            LaubeException: KronosExceptionが発生時にThrowします。
            ArtemisException: ArtemisExceptionが発生時にThrowします。
            Exception: Exceptionが発生時にThrowします。
        """
        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException(self.E002)

            # 規定申請書マスタ
            applicationFormDao = ApplicationFormDao()
            self.applicationForm_list = applicationFormDao.find_all_company_code(session, company_code)

            if self.applicationForm_list is None:
                raise LaubeException(self.E006)

            # 申請書別ルートマスタ
            applicationFormRouteDao = ApplicationFormRouteDao()
            self.applicationFormRoute_list = applicationFormRouteDao.find_all_company_code(session, company_code)

            # 申請分類マスタ
            applicationClassificationDao = ApplicationClassificationDao()
            self.applicationClassification_list = applicationClassificationDao.find_all_company_code(session, company_code)

            if self.applicationClassification_list is None:
                raise LaubeException(self.E011)

            bossDao = BossDao()
            self.boss_list = bossDao.find_all_company_code(session, company_code)

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    """
    [利用場所]
    申請画面のInitAPIにて呼び出される事を想定しています。
    [Unit Test 済]
    [機能]
    上司マスタの登録ができていない従業員が新規申請を行う際、上司入力欄を表示させる必要がある申請かを判定してくれます。

    Args:
        session               [必須] : セッション情報
        target_company_code   [必須] : 会社コード[対象者]
        target_group_code     [必須] : 部署コード[対象者]
        target_employee_code  [必須] : 従業員番号[対象者]
        application_form_code [必須] : 申請書コード

    returns:
        True 「上司入力欄」を表示して下さい。
        False 「上司入力欄」を表示させず、get_application_infoメソッドを呼び出して下さい。

    Raises:
        LaubeException : Laube例外
    """
    def is_display_boss_field(self, session, target_company_code, target_group_code, target_employee_code, application_form_code):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not target_company_code:
                raise LaubeException(self.E002)

            if not target_group_code:
                raise LaubeException(self.E003)

            if not target_employee_code:
                raise LaubeException(self.E004)

            if not application_form_code:
                raise LaubeException(self.E005)

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, target_company_code)

            applicationForm = next((someone for someone in self.applicationForm_list if someone.application_form_code == application_form_code), None)

            if applicationForm is None:
                raise LaubeException(self.E006)

            # 直接部門フラグの設定が「なし」の場合、間接部門ルートのみの申請書なので上司入力欄は不要です。
            if applicationForm.route_flag == RouteFlag.NO_INDIVIDUAL_ROUTE:
                return False

            elif applicationForm.route_flag == RouteFlag.INDIVIDUAL_ROUTE:

                applicationFormRoute = next((someone for someone in self.applicationFormRoute_list if someone.application_form_code == application_form_code and someone.group_code == target_group_code), None)

                if applicationFormRoute is None:
                    # レコードが見つからない場合、部署コードをNoneで再検索します。
                    # ※直接部門ルートは、[部署単位]又は[全体]の何れかで設定可能な為
                    applicationFormRoute = next((someone for someone in self.applicationFormRoute_list if someone.application_form_code == application_form_code and someone.group_code is None), None)

                    # 直接部門ルートが登録されている場合、上司ルートは使わないので上司入力欄は不要です。
                    if applicationFormRoute is not None:
                        if applicationFormRoute.individual_route_code is not None and len(applicationFormRoute.individual_route_code.strip()) > 0:
                            return False
                        else:
                            pass
                    else:
                        pass
                else:
                    # 直接部門ルートが登録されている場合、上司ルートは使わないので上司入力欄は不要です。
                    if applicationFormRoute.individual_route_code is not None and len(applicationFormRoute.individual_route_code.strip()) > 0:
                        return False
                    else:
                        pass

            elif applicationForm.route_flag == RouteFlag.BOSS_ROUTE:

                # 会社コード[申請者]/部署コード[申請者]/従業員番号[申請者]/申請書コードにて上司マスタを検索します。
                boss = next((someone for someone in self.boss_list if someone.group_code == target_group_code and someone.employee_code == target_employee_code and someone.application_form_code == application_form_code), None)

                if boss is None:
                    # 上司マスタにレコードが無い為、申請書コードがブランクのレコードを再検索します。
                    boss = next((someone for someone in self.boss_list if someone.group_code == target_group_code and someone.employee_code == target_employee_code and someone.application_form_code is None), None)

                    if boss is None:
                        # 上司マスタにレコードが無い為、部署コードがブランクのレコードを再検索します。
                        boss = next((someone for someone in self.boss_list if someone.group_code is None and someone.employee_code == target_employee_code and someone.application_form_code == application_form_code), None)

                        if boss is None:
                            # 上司マスタにレコードが無い為、部署コードと申請書コードがブランクのレコードを再検索します。
                            boss = next((someone for someone in self.boss_list if someone.group_code is None and someone.employee_code == target_employee_code and someone.application_form_code is None), None)

                            if boss is None:
                                # 上司マスタが未設定と思われる為、Trueを返却します。
                                return True
                return False

            else:
                raise LaubeException(self.E007)

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    申請画面のInitAPIにて呼び出される事を想定しています。

    [機能]
    申請モード1 [下書き/申請] 時の承認ルートを返却します。

    [前提]
    本メソッドを呼び出す前に必ず、is_display_boss_fieldメソッドを呼出してチェックを行って下さい。

    Args:
        session                 [必須] : セッション情報
        application_form_code   [必須] : 申請書コード
        target_company_code     [必須] : 会社コード[対象者]
        target_group_code       [必須] : 部署コード[対象者]
        target_employee_code    [必須] : 従業員番号[対象者]
        boss_group_code         [任意] : 部署コード[上司]
        boos_employee_code      [任意] : 従業員番号[上司]
        applicant_company_code  [必須] : 会社コード[申請者]
        applicant_group_code    [必須] : 部署コード[申請者]
        applicant_employee_code [必須] : 従業員番号[申請者]

    Returns:
        ルート情報

    Raises:
        LaubeException : Laube例外
    """
    def get_application_info(self, session, application_form_code, target_company_code, target_group_code, target_employee_code, boss_group_code, boos_employee_code, applicant_company_code, applicant_group_code, applicant_employee_code):

        applicationInfoDto = ApplicationInfoDto()

        try:
            if not session:
                raise LaubeException(self.E001)

            if not application_form_code:
                raise LaubeException(self.E005)

            if not target_company_code:
                raise LaubeException(self.E002)

            if not target_group_code:
                raise LaubeException(self.E003)

            if not target_employee_code:
                raise LaubeException(self.E004)

            if not applicant_company_code:
                raise LaubeException(self.E008)

            if not applicant_group_code:
                raise LaubeException(self.E009)

            if not applicant_employee_code:
                raise LaubeException(self.E010)

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, target_company_code)

            system_date = datetime.now()

            # 対象者の情報 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            # 会社コード[対象者]/申請書コードにて申請書マスタを検索します。
            applicationForm = next((someone for someone in self.applicationForm_list if someone.application_form_code == application_form_code), None)

            if applicationForm is None:
                raise LaubeException(self.E006)

            applicationInfoDto.screen_mode = ScreenMode.APPLY_MODE_1  # 申請モード1　[下書き/申請]

            applicationInfoDto.application_form_code = application_form_code
            applicationInfoDto.application_form_name, applicationInfoDto.application_classification_code, applicationInfoDto.application_classification_name = self.__get_application_form_name(session, target_company_code, application_form_code)
            applicationInfoDto.target_company_code = target_company_code
            applicationInfoDto.target_company_name = self.__get_company_name(session, target_company_code)
            applicationInfoDto.target_group_code = target_group_code
            applicationInfoDto.target_group_name = self.__get_group_name(session, target_company_code, target_group_code)
            applicationInfoDto.target_employee_code = target_employee_code
            applicationInfoDto.target_employee_name = self.__get_employee_name(session, target_company_code, target_employee_code)

            # 申請者の情報 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            # 会社コード[申請者]にて会社マスタを検索します。
            applicationInfoDto.applicant_company_code = applicant_company_code
            applicationInfoDto.applicant_company_name = self.__get_company_name(session, applicant_company_code)
            applicationInfoDto.applicant_group_code = applicant_group_code
            applicationInfoDto.applicant_group_name = self.__get_group_name(session, applicant_company_code, applicant_group_code)
            applicationInfoDto.applicant_employee_code = applicant_employee_code
            applicationInfoDto.applicant_employee_name = self.__get_employee_name(session, applicant_company_code, applicant_employee_code)

            # 承認ルート情報 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            applicationInfoDto.approverl_list = list()

            # 会社コード[対象者]/申請書コードにて申請書マスタを検索します。
            applicationForm = next((someone for someone in self.applicationForm_list if someone.application_form_code == application_form_code), None)

            if applicationForm is None:
                raise LaubeException(self.E006)

            # 会社コード[対象者]/申請書コードにて申請分類マスタを検索します。
            applicationClassification = next((someone for someone in self.applicationClassification_list if someone.application_classification_code == applicationForm.application_classification_code), None)

            if applicationClassification is None:
                raise LaubeException(self.E011)

            # 会社コード[対象者]/部署コード[対象者]/申請書コードにて申請書別ルートマスタを検索します。
            applicationFormRoute = next((someone for someone in self.applicationFormRoute_list if someone.application_form_code == application_form_code and someone.group_code == target_group_code), None)

            if applicationFormRoute is None:
                # レコードが見つからない場合、部署コード=Noneで再検索します。
                applicationFormRoute = next((someone for someone in self.applicationFormRoute_list if someone.application_form_code == application_form_code and someone.group_code is None), None)

            # 直接部門ルートを検索します。

            # 申請書マスタの直接部門フラグが「あり」の場合
            if applicationForm.route_flag == RouteFlag.INDIVIDUAL_ROUTE:

                if applicationFormRoute is None or applicationFormRoute.individual_route_code is None or len(applicationFormRoute.individual_route_code.strip()) == 0:
                    pass
                else:
                    applicationInfoDto.approverl_list = self.__get_individual_approverl_list(session, target_company_code, applicationFormRoute.individual_route_code, applicationForm)

            else:
                # 直接部門フラグ「上司ルート」の場合
                if applicationForm.route_flag == RouteFlag.BOSS_ROUTE:
                    applicationInfoDto.approverl_list = self.__get_boss_approverl_list(session, target_company_code, target_group_code, target_employee_code, application_form_code, boss_group_code, boos_employee_code, applicationForm.job_title_code)

                    # 承認ルートが空になった場合、申請分類マスタの直接部門ルートコードにて再取得します。(JSOX対応)
                    if (applicationInfoDto.approverl_list is None or len(applicationInfoDto.approverl_list) == 0):
                        applicationInfoDto.approverl_list = self.__get_individual_approverl_list(session, target_company_code, applicationClassification.individual_route_code, applicationForm)

                # 直接部門ルートが「なし」の場合
                else:
                    applicationInfoDto.approverl_list = list()

            # 申請書マスタの「申請者を承認から外す判定」が真の場合、申請者を承認ルートから削除します。

            # 承認者の中に申請者がいるか確認します。
            _has_applicant_user = False
            for approverlDataInfo in applicationInfoDto.approverl_list:
                approverlDataInfoDto = ApproverlDataInfoDto()
                if approverlDataInfo.approverl_company_code == applicant_company_code and approverlDataInfo.approverl_group_code == applicant_group_code and approverlDataInfo.approverl_employee_code == applicant_employee_code:
                    _has_applicant_user = True
                    break

            approverl_list = list()
            if applicationForm.skip_apply_employee is True and _has_applicant_user:

                # 申請者が直接部門ルートに存在する場合、そこまでの審査者を承認済とします。
                _is_processed_applicant_user = False

                number = 0
                for approverlDataInfo in applicationInfoDto.approverl_list:

                    approverlDataInfoDto = ApproverlDataInfoDto()

                    if approverlDataInfo.approverl_company_code == applicant_company_code and approverlDataInfo.approverl_employee_code == applicant_employee_code:
                        approverlDataInfoDto.reaching_date = system_date  # 到達日
                        approverlDataInfoDto.process_date = system_date  # 処理日
                        approverlDataInfoDto.activity_status = ActivityStatus.AUTHORIZER_AUTOMATIC_APPROVAL  # 自動承認
                        approverlDataInfoDto.approval_function = ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL
                        approverlDataInfoDto.approverl_comment = '審査者が申請者の同一の為、自動承認します'  # 承認者のコメント
                        _is_processed_applicant_user = True
                    else:
                        if _is_processed_applicant_user:
                            approverlDataInfoDto.reaching_date = None  # 到達日
                            approverlDataInfoDto.process_date = None  # 処理日
                            approverlDataInfoDto.activity_status = ActivityStatus.AUTHORIZER_UNTREATED  # 未処理
                            approverlDataInfoDto.approval_function = approverlDataInfo.approval_function
                            approverlDataInfoDto.approverl_comment = None  # 承認者のコメント
                        else:
                            approverlDataInfoDto.reaching_date = system_date  # 到達日
                            approverlDataInfoDto.process_date = system_date  # 処理日
                            approverlDataInfoDto.activity_status = ActivityStatus.AUTHORIZER_AUTOMATIC_APPROVAL  # 自動承認
                            approverlDataInfoDto.approval_function = ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL
                            approverlDataInfoDto.approverl_comment = '審査者の後続に申請者がいる為、自動承認します'  # 承認者のコメント

                    approverlDataInfoDto.company_code = approverlDataInfo.company_code
                    approverlDataInfoDto.company_name = self.__get_company_name(session, approverlDataInfo.company_code)
                    approverlDataInfoDto.application_number = None
                    approverlDataInfoDto.target_company_code = target_company_code  # 対象者の会社コード
                    approverlDataInfoDto.target_company_name = self.__get_company_name(session, target_company_code)  # 対象者の会社名
                    approverlDataInfoDto.target_group_code = target_group_code  # 対象者の部署コード
                    approverlDataInfoDto.target_group_name = self.__get_group_name(session, target_company_code, target_group_code)  # 対象者の部署名
                    approverlDataInfoDto.target_employee_code = target_employee_code  # 対象者の従業員番号
                    approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, target_company_code, target_employee_code)  # 対象者の従業員名
                    approverlDataInfoDto.applicant_company_code = applicant_company_code  # 申請者の会社コード
                    approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, applicant_company_code)  # 申請者の会社名
                    approverlDataInfoDto.applicant_group_code = applicant_group_code  # 申請者の部署コード
                    approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, applicant_company_code, applicant_group_code)  # 申請者の部署名
                    approverlDataInfoDto.applicant_employee_code = applicant_employee_code  # 申請者の従業員番号
                    approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, applicant_company_code, applicant_employee_code)  # 申請者の従業員名
                    approverlDataInfoDto.apply_date = None  # 申請日
                    approverlDataInfoDto.application_status = None  # 申請書ステータス
                    approverlDataInfoDto.route_type = RouteType.INDIVIDUAL_ROUTE
                    number += 1
                    approverlDataInfoDto.route_number = number
                    approverlDataInfoDto.approverl_company_code = approverlDataInfo.approverl_company_code
                    approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, approverlDataInfo.approverl_company_code)

                    approverlDataInfoDto.approverl_role_code = approverlDataInfo.approverl_role_code
                    if approverlDataInfoDto.approverl_role_code is None or len(approverlDataInfoDto.approverl_role_code.strip()) == 0:
                        approverlDataInfoDto.approverl_role_name = None
                    else:
                        roleDao = RoleDao()
                        role = roleDao.find_ix_m_role(session, approverlDataInfoDto.approverl_company_code, approverlDataInfoDto.approverl_role_code)

                        if role is None:
                            raise LaubeException(f'role record is missing. key={approverlDataInfoDto.approverl_company_code}, {approverlDataInfoDto.approverl_role_code}')

                        approverlDataInfoDto.approverl_role_name = role.role_name

                    approverlDataInfoDto.approverl_group_code = approverlDataInfo.approverl_group_code
                    approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, approverlDataInfo.approverl_company_code, approverlDataInfo.approverl_group_code)
                    approverlDataInfoDto.approverl_employee_code = approverlDataInfo.approverl_employee_code
                    approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, approverlDataInfo.approverl_company_code, approverlDataInfo.approverl_employee_code)
                    approverlDataInfoDto.deputy_approverl_company_code = None  # 会社コード[代理承認者]
                    approverlDataInfoDto.deputy_approverl_company_name = None  # 会社名[代理承認者]
                    approverlDataInfoDto.deputy_approverl_group_code = None  # 部署コード[代理承認者]
                    approverlDataInfoDto.deputy_approverl_group_name = None  # 代理承認者の部署名
                    approverlDataInfoDto.deputy_approverl_employee_code = None  # 従業員番号[代理承認者]
                    approverlDataInfoDto.deputy_approverl_employee_name = None  # 従業員名[代理承認者]
                    approverlDataInfoDto.deputy_contents = None  # 依頼理由
                    approverl_list.append(approverlDataInfoDto)

                applicationInfoDto.approverl_list = approverl_list

            if applicationFormRoute is None or applicationFormRoute.common_route_code is None or len(applicationFormRoute.common_route_code.strip()) == 0:
                pass
            else:
                # 間接部門ルートを検索します。
                applicationInfoDto.approverl_list = self.__get_common_approverl_list(session, target_company_code, applicationFormRoute.common_route_code, applicationInfoDto.approverl_list)

            return applicationInfoDto

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    get_application_infoメソッド内から呼び出される事を想定しています。

    [機能]
    個別アクティビティマスタを検索し承認ルートを取得します。
    もしアクティビティマスタに利用権限コードが設定されていた場合は利用権限コードをもとに従業員利用権限マスタを検索し該当の従業員を全て承認ルートに加えます。

    Args:
        session: セッション情報
        target_company_code: 会社コード[対象者]
        individual_route_code: 直接部門ルートコード
        applicationForm: 申請書マスタ

    Returns:
        approverl_list

    Raises:
        LaubeException : Laube例外
    """
    def __get_individual_approverl_list(self, session, target_company_code, individual_route_code, applicationForm):

        try:

            utility = Utility()

            if not session:
                raise LaubeException(self.E001)

            if not target_company_code:
                raise LaubeException(self.E002)

            if not individual_route_code:
                return list()

            if applicationForm is None:
                raise LaubeException(self.E006)

            dt = datetime.now()
            system_date = utility.convert_datetime_2_date(dt)

            individualActivityDao = IndividualActivityDao()
            individual_activity_list = individualActivityDao.find_all_company_code_individual_route_code(session, target_company_code, individual_route_code)

            if individual_activity_list is None:
                return list()

            approverl_list = list()
            _route_employee_code_list = list()

            for individual_activity in individual_activity_list:

                # 指定されている部署および従業員の存在チェックを実施
                if individual_activity.approverl_role_code is None or len(individual_activity.approverl_role_code.strip()) == 0:

                    employeeDao = EmployeeDao()
                    employee = employeeDao.find_availability_employee(session, individual_activity.company_code, individual_activity.approverl_employee_code, date.today())

                    if employee is None:
                        raise LaubeException(self.E012)

                    #  承認者の利用権限コードがNone
                    employeeGroupDao = EmployeeGroupDao()
                    employeeGroup = employeeGroupDao.find_ix_m_employee_group(session, individual_activity.company_code, individual_activity.approverl_employee_code, individual_activity.approverl_group_code)

                    if employeeGroup is None:
                        raise LaubeException(self.E012)

                    if employeeGroup.term_to is None or employeeGroup.term_to >= date.today():
                        pass
                    else:
                        raise LaubeException(self.E012)

                    if employee.logical_deletion:
                        continue

                    if (employee.retirement_date is not None) and (employee.retirement_date < system_date):
                        continue

                approverlDataInfoDto = ApproverlDataInfoDto()
                approverlDataInfoDto.company_code = individual_activity.company_code
                approverlDataInfoDto.company_name = self.__get_company_name(session, individual_activity.company_code)

                approverlDataInfoDto.application_number = None
                approverlDataInfoDto.route_type = RouteType.INDIVIDUAL_ROUTE
                approverlDataInfoDto.route_number = individual_activity.activity_code
                approverlDataInfoDto.approverl_company_code = individual_activity.approverl_company_code
                approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, individual_activity.approverl_company_code)

                approverlDataInfoDto.approverl_role_code = individual_activity.approverl_role_code

                if approverlDataInfoDto.approverl_role_code is None or len(approverlDataInfoDto.approverl_role_code.strip()) == 0:
                    approverlDataInfoDto.approverl_role_name = None
                else:
                    roleDao = RoleDao()
                    role = roleDao.find_ix_m_role(session, approverlDataInfoDto.approverl_company_code, approverlDataInfoDto.approverl_role_code)

                    if role is None:
                        raise LaubeException(f'role record is missing. key={approverlDataInfoDto.approverl_company_code},{approverlDataInfoDto.approverl_role_code}')

                    approverlDataInfoDto.approverl_role_name = role.role_name

                approverlDataInfoDto.approverl_group_code = individual_activity.approverl_group_code
                approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, individual_activity.approverl_company_code, individual_activity.approverl_group_code)
                approverlDataInfoDto.approverl_employee_code = individual_activity.approverl_employee_code
                approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, individual_activity.approverl_company_code, individual_activity.approverl_employee_code)
                approverlDataInfoDto.deputy_approverl_company_code = None  # 会社コード[代理承認者]
                approverlDataInfoDto.deputy_approverl_company_name = None  # 会社名[代理承認者]
                approverlDataInfoDto.deputy_approverl_group_code = None  # 部署コード[代理承認者]
                approverlDataInfoDto.deputy_approverl_group_name = None  # 代理承認者の部署名
                approverlDataInfoDto.deputy_approverl_employee_code = None  # 従業員番号[代理承認者]
                approverlDataInfoDto.deputy_approverl_employee_name = None  # 従業員名[代理承認者]
                approverlDataInfoDto.deputy_contents = None  # 依頼理由
                approverlDataInfoDto.reaching_date = None  # 到達日
                approverlDataInfoDto.process_date = None  # 処理日
                approverlDataInfoDto.activity_status = ActivityStatus.AUTHORIZER_UNTREATED  # 未処理
                approverlDataInfoDto.approverl_comment = None  # 承認者のコメント

                approverlDataInfoDto.approval_function = individual_activity.function

                # 自動承認フラグ=自動承認の場合
                if AutoApproverlFlag.AUTOMATIC_APPROVAL == applicationForm.auto_approverl_flag:
                    for _route_employee_code in _route_employee_code_list:
                        if _route_employee_code == individual_activity.approverl_employee_code:  # 既にルート上に存在する従業員の場合
                            approverlDataInfoDto.approval_function = ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL  # 自動承認を設定
                            break
                        else:
                            continue

                    _route_employee_code_list.append(individual_activity.approverl_employee_code)

                approverl_list.append(approverlDataInfoDto)

            return approverl_list

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    """
    [利用場所]
    get_application_infoメソッド内から呼び出される事を想定しています。

    [機能]
    上司ルートを取得します。

    Args:
        session : セッション情報
        target_company_code: 会社コード[対象者]
        target_group_code: 部署コード[対象者]
        target_employee_code: 従業員番号[対象者]
        application_form_code: 申請書コード
        boss_group_code: 画面で入力した部署コード[上司]
        boos_employee_code: 画面で入力した従業員番号[上司]
        job_title_code: 職名コード

    Returns:
        approverl_list

    Raises:
        LaubeException : Laube例外
    """
    def __get_boss_approverl_list(self, session, target_company_code, target_group_code, target_employee_code, application_form_code, boss_group_code, boos_employee_code, job_title_code):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not target_company_code:
                raise LaubeException(self.E002)

            if not target_group_code:
                raise LaubeException(self.E003)

            if not target_employee_code:
                raise LaubeException(self.E004)

            if not application_form_code:
                raise LaubeException(self.E005)

            approverl_list = list()
            number = 0
            w_boss_company_code = None
            w_boss_group_code = None
            w_boos_employee_code = None

            # 申請画面より上司が入力されているか確認します
            is_entry_boss = (boss_group_code is not None and len(boss_group_code.strip()) > 0) and (boos_employee_code is not None and len(boos_employee_code.strip()) > 0)

            if is_entry_boss:
                employeeGroupDao = EmployeeGroupDao()
                employeeGroup = employeeGroupDao.find_ix_m_employee_group(session, target_company_code, boos_employee_code, boss_group_code)

                if employeeGroup is None:
                    raise LaubeException(f'employee_group record is missing. key={target_company_code},{boss_group_code},{boos_employee_code}')

                w_boss_company_code = employeeGroup.company_code
                w_boss_group_code = employeeGroup.group_code
                w_boos_employee_code = employeeGroup.employee_code

                # 直接部門ルートに追加します。
                approverlDataInfoDto = ApproverlDataInfoDto()
                approverlDataInfoDto.company_code = target_company_code
                approverlDataInfoDto.company_name = self.__get_company_name(session, target_company_code)
                approverlDataInfoDto.application_number = None
                approverlDataInfoDto.route_type = RouteType.INDIVIDUAL_ROUTE
                approverlDataInfoDto.route_number = number + 1
                approverlDataInfoDto.approverl_company_code = employeeGroup.company_code
                approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, employeeGroup.company_code)
                approverlDataInfoDto.approverl_role_code = None
                approverlDataInfoDto.approverl_role_name = None
                approverlDataInfoDto.approverl_group_code = employeeGroup.group_code
                approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, employeeGroup.company_code, employeeGroup.group_code)
                approverlDataInfoDto.approverl_employee_code = employeeGroup.employee_code
                approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, employeeGroup.company_code, employeeGroup.employee_code)
                approverlDataInfoDto.deputy_approverl_company_code = None
                approverlDataInfoDto.deputy_approverl_company_name = None
                approverlDataInfoDto.deputy_approverl_group_code = None
                approverlDataInfoDto.deputy_approverl_group_name = None
                approverlDataInfoDto.deputy_approverl_employee_code = None
                approverlDataInfoDto.deputy_approverl_employee_name = None
                approverlDataInfoDto.deputy_contents = None
                approverlDataInfoDto.reaching_date = None
                approverlDataInfoDto.process_date = None
                approverlDataInfoDto.activity_status = ActivityStatus.AUTHORIZER_UNTREATED
                approverlDataInfoDto.approverl_comment = None
                approverlDataInfoDto.approval_function = ApprovalFunction.EXAMINATION

                approverl_list.append(approverlDataInfoDto)

            else:
                # 会社コード[申請者]/部署コード[申請者]/従業員番号[申請者]/申請書コードにて上司マスタを検索します。
                boss = next((someone for someone in self.boss_list if someone.group_code == target_group_code and someone.employee_code == target_employee_code and someone.application_form_code == application_form_code), None)

                if boss is None:
                    # 上司マスタにレコードが無い為、申請書コードがブランクのレコードを再検索します。
                    boss = next((someone for someone in self.boss_list if someone.group_code == target_group_code and someone.employee_code == target_employee_code and someone.application_form_code is None), None)

                    if boss is None:
                        # 上司マスタにレコードが無い為、部署コードがブランクのレコードを再検索します。
                        boss = next((someone for someone in self.boss_list if someone.group_code is None and someone.employee_code == target_employee_code and someone.application_form_code == application_form_code), None)

                        if boss is None:
                            # 上司マスタにレコードが無い為、部署コードと申請書コードがブランクのレコードを再検索します。
                            boss = next((someone for someone in self.boss_list if someone.group_code is None and someone.employee_code == target_employee_code and someone.application_form_code is None), None)

                            if boss is None:
                                # 上司マスタが未設定と思われる為、Trueを返却します。
                                return None

                is_boss_company = boss.boss_company_code is None or len(boss.boss_company_code.strip()) == 0
                is_boss_group_code = boss.boss_group_code is None or len(boss.boss_group_code.strip()) == 0
                is_boss_employee_code = boss.boss_employee_code is None or len(boss.boss_employee_code.strip()) == 0

                if is_boss_company is True and is_boss_group_code is True and is_boss_employee_code is True:
                    return approverl_list

                w_boss_company_code = boss.boss_company_code
                w_boss_group_code = boss.boss_group_code
                w_boos_employee_code = boss.boss_employee_code
                approverlDataInfoDto = ApproverlDataInfoDto()
                approverlDataInfoDto.company_code = target_company_code
                approverlDataInfoDto.company_name = self.__get_company_name(session, target_company_code)
                approverlDataInfoDto.application_number = None
                approverlDataInfoDto.route_type = RouteType.INDIVIDUAL_ROUTE
                number = number + 1
                approverlDataInfoDto.route_number = number
                approverlDataInfoDto.approverl_company_code = boss.boss_company_code
                approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, boss.boss_company_code)
                approverlDataInfoDto.approverl_role_code = None
                approverlDataInfoDto.approverl_role_name = None
                approverlDataInfoDto.approverl_group_code = boss.boss_group_code
                approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, boss.boss_company_code, boss.boss_group_code)
                approverlDataInfoDto.approverl_employee_code = boss.boss_employee_code
                approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, boss.boss_company_code, boss.boss_employee_code)
                approverlDataInfoDto.deputy_approverl_company_code = None
                approverlDataInfoDto.deputy_approverl_company_name = None
                approverlDataInfoDto.deputy_approverl_group_code = None
                approverlDataInfoDto.deputy_approverl_group_name = None
                approverlDataInfoDto.deputy_approverl_employee_code = None
                approverlDataInfoDto.deputy_approverl_employee_name = None
                approverlDataInfoDto.deputy_contents = None
                approverlDataInfoDto.reaching_date = None
                approverlDataInfoDto.process_date = None
                approverlDataInfoDto.activity_status = ActivityStatus.AUTHORIZER_UNTREATED
                approverlDataInfoDto.approverl_comment = None
                approverlDataInfoDto.approval_function = ApprovalFunction.EXAMINATION

                approverl_list.append(approverlDataInfoDto)

                is_escape = False

                if job_title_code is None or len(job_title_code.strip()) == 0:
                    is_escape = False
                else:
                    # 指定されている職名を持つ場合、そこで終了します。
                    employeeJobTitleDao = EmployeeJobTitleDao()
                    employeeJobTitles = employeeJobTitleDao.find_all_company_code_employee_code(session, w_boss_company_code, w_boos_employee_code)

                    if employeeJobTitles is None:
                        pass

                    for employeeJobTitle in employeeJobTitles:
                        if employeeJobTitle.job_title_code == job_title_code:
                            is_escape = True
                            break

                if is_escape:
                    pass
                else:
                    # 最上位の上司が見つかるまで繰り返す
                    while True:

                        bossDao = BossDao()
                        # 会社コード/部署コード/従業員番号/申請書コードにて上司マスタを検索します。
                        boss = bossDao.find_ix_m_boss(session, w_boss_company_code, w_boss_group_code, w_boos_employee_code, application_form_code)

                        if boss is None:
                            # 上司マスタにレコードが無い為、申請書コードがブランクのレコードを再検索します。
                            boss = bossDao.find_ix_m_boss(session, w_boss_company_code, w_boss_group_code, w_boos_employee_code, None)

                            if boss is None:
                                # 上司マスタにレコードが無い為、部署コードがブランクのレコードを再検索します。
                                boss = bossDao.find_ix_m_boss(session, w_boss_company_code, None, w_boos_employee_code, application_form_code)

                                if boss is None:
                                    boss = bossDao.find_ix_m_boss(session, w_boss_company_code, None, w_boos_employee_code, None)

                                    if boss is None:
                                        # 上司マスタが未設定の為、終了します。
                                        break

                        if boss.boss_employee_code is None or len(boss.boss_employee_code.strip()) == 0:
                            break

                        w_boss_company_code = boss.boss_company_code
                        w_boss_group_code = boss.boss_group_code
                        w_boos_employee_code = boss.boss_employee_code

                        approverlDataInfoDto = ApproverlDataInfoDto()
                        approverlDataInfoDto.company_code = target_company_code
                        approverlDataInfoDto.company_name = self.__get_company_name(session, target_company_code)

                        approverlDataInfoDto.application_number = None
                        approverlDataInfoDto.route_type = RouteType.INDIVIDUAL_ROUTE
                        number = number + 1
                        approverlDataInfoDto.route_number = number
                        approverlDataInfoDto.approverl_company_code = boss.boss_company_code
                        approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, boss.boss_company_code)

                        approverlDataInfoDto.approverl_role_code = None
                        approverlDataInfoDto.approverl_role_name = None
                        approverlDataInfoDto.approverl_group_code = boss.boss_group_code
                        approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, boss.boss_company_code, boss.boss_group_code)
                        approverlDataInfoDto.approverl_employee_code = boss.boss_employee_code
                        approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, boss.boss_company_code, boss.boss_employee_code)
                        approverlDataInfoDto.deputy_approverl_company_code = None  # 会社コード[代理承認者]
                        approverlDataInfoDto.deputy_approverl_company_name = None  # 会社名[代理承認者]
                        approverlDataInfoDto.deputy_approverl_group_code = None  # 部署コード[代理承認者]
                        approverlDataInfoDto.deputy_approverl_group_name = None  # 代理承認者の部署名
                        approverlDataInfoDto.deputy_approverl_employee_code = None  # 従業員番号[代理承認者]
                        approverlDataInfoDto.deputy_approverl_employee_name = None  # 従業員名[代理承認者]
                        approverlDataInfoDto.deputy_contents = None  # 依頼理由
                        approverlDataInfoDto.reaching_date = None  # 到達日
                        approverlDataInfoDto.process_date = None  # 処理日
                        approverlDataInfoDto.activity_status = ActivityStatus.AUTHORIZER_UNTREATED  # 未処理
                        approverlDataInfoDto.approverl_comment = None  # 承認者のコメント
                        approverlDataInfoDto.approval_function = ApprovalFunction.EXAMINATION

                        # 上司マスタが永久ループになるパターンを排除
                        if approverl_list is not None and len(approverl_list) > 0:
                            for w_boss in approverl_list:
                                if (w_boss.approverl_group_code + w_boss.approverl_employee_code) == (boss.boss_group_code + boss.boss_employee_code):
                                    raise LaubeException('Laube-W002')  # 上司マスタの設定を見直して下さい

                        approverl_list.append(approverlDataInfoDto)

                        if job_title_code is None or len(job_title_code.strip()) == 0:
                            continue
                        else:
                            # 指定されている職名を持つ場合、そこで終了します。
                            employeeJobTitleDao = EmployeeJobTitleDao()
                            employeeJobTitles = employeeJobTitleDao.find_all_company_code_employee_code(session, boss.boss_company_code, boss.boss_employee_code)

                            if employeeJobTitles is None:
                                continue

                            for employeeJobTitle in employeeJobTitles:
                                if employeeJobTitle.job_title_code == job_title_code:
                                    return approverl_list

            return approverl_list

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    """
    [利用場所]
    get_application_infoメソッド内から呼び出される事を想定しています。

    [機能]
    共通アクティビティマスタを検索し承認ルートを取得します。
    もしアクティビティマスタに利用権限コードが設定されていた場合は利用権限コードをもとに従業員利用権限マスタを検索し該当の従業員を全て承認ルートに加えます。

    Args:
        session: セッション情報
        applocation_forme_code: 申請書コード
        target_company_code: 会社コード[対象者]
        common_route_code: 間接部門ルートコード
        approverl_list: 承認ルート

    Returns:
        ルート情報

    Raises:
        LaubeException : Laube例外
    """
    def __get_common_approverl_list(self, session, target_company_code, common_route_code, approverl_list):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not target_company_code:
                raise LaubeException(self.E002)

            if not common_route_code:
                raise LaubeException('required common_route_code')

            commonActivityDao = CommonActivityDao()
            common_activity_list = commonActivityDao.find_all_company_code_common_route_code(session, target_company_code, common_route_code)

            if common_activity_list is None:
                raise LaubeException(f'common_activity record is missing. key={target_company_code},{common_route_code}')

            for common_activity in common_activity_list:

                # 指定されている部署および従業員の存在チェックを実施
                if common_activity.approverl_role_code is None:

                    employeeDao = EmployeeDao()
                    employee = employeeDao.find_availability_employee(session, common_activity.company_code, common_activity.approverl_employee_code, date.today())

                    if employee is None:
                        raise LaubeException(self.E012)

                    #  承認者の利用権限コードがNone
                    employeeGroupDao = EmployeeGroupDao()
                    employeeGroup = employeeGroupDao.find_ix_m_employee_group(session, common_activity.company_code, common_activity.approverl_employee_code, common_activity.approverl_group_code)

                    if employeeGroup is None:
                        raise LaubeException(self.E012)

                    if employeeGroup.term_to is None or employeeGroup.term_to >= date.today():
                        pass
                    else:
                        raise LaubeException(self.E012)

                approverlDataInfoDto = ApproverlDataInfoDto()
                approverlDataInfoDto.company_code = target_company_code
                approverlDataInfoDto.company_name = self.__get_company_name(session, target_company_code)

                approverlDataInfoDto.application_number = None
                approverlDataInfoDto.route_type = RouteType.COMMON_ROUTE
                approverlDataInfoDto.route_number = common_activity.activity_code
                approverlDataInfoDto.approverl_company_code = common_activity.approverl_company_code
                approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, common_activity.approverl_company_code)

                approverlDataInfoDto.approverl_role_code = common_activity.approverl_role_code

                if approverlDataInfoDto.approverl_role_code is None or len(approverlDataInfoDto.approverl_role_code.strip()) == 0:
                    approverlDataInfoDto.approverl_role_name = None
                else:
                    roleDao = RoleDao()
                    role = roleDao.find_ix_m_role(session, approverlDataInfoDto.approverl_company_code, approverlDataInfoDto.approverl_role_code)

                    if role is None:
                        raise LaubeException(f'role record is missing. key={approverlDataInfoDto.approverl_company_code},{approverlDataInfoDto.approverl_role_code}')

                    approverlDataInfoDto.approverl_role_name = role.role_name

                approverlDataInfoDto.approverl_group_code = common_activity.approverl_group_code
                approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, common_activity.approverl_company_code, common_activity.approverl_group_code)
                approverlDataInfoDto.approverl_employee_code = common_activity.approverl_employee_code
                approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, common_activity.approverl_company_code, common_activity.approverl_employee_code)
                approverlDataInfoDto.deputy_approverl_company_code = None  # 会社コード[代理承認者]
                approverlDataInfoDto.deputy_approverl_company_name = None  # 会社名[代理承認者]
                approverlDataInfoDto.deputy_approverl_group_code = None  # 部署コード[代理承認者]
                approverlDataInfoDto.deputy_approverl_group_name = None  # 代理承認者の部署名
                approverlDataInfoDto.deputy_approverl_employee_code = None  # 従業員番号[代理承認者]
                approverlDataInfoDto.deputy_approverl_employee_name = None  # 従業員名[代理承認者]
                approverlDataInfoDto.deputy_contents = None  # 依頼理由
                approverlDataInfoDto.reaching_date = None  # 到達日
                approverlDataInfoDto.process_date = None  # 処理日
                approverlDataInfoDto.activity_status = ActivityStatus.AUTHORIZER_UNTREATED  # 未処理
                approverlDataInfoDto.approverl_comment = None  # 承認者のコメント
                approverlDataInfoDto.approval_function = common_activity.function
                approverl_list.append(approverlDataInfoDto)

            return approverl_list

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    """
    [利用場所]
    申請一覧画面のViewAPIにて呼び出される事を想定しています。
    申請状況画面のViewAPIにて呼び出される事を想定しています。

    [機能]
    申請一覧の取得を行います。
    申請状況の取得を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        target_company_code : 会社コード[対象者]
        target_group_code : 部署コード[対象者]
        target_employee_code : 従業員番号[対象者]
        application_number_list : 申請番号のリスト
        re_application_number : 再申請番号
        application_classification_code_list : 申請分類コードのリスト
        application_status_list : 申請書ステータスのリスト
        apply_date_from : 申請日_から
        apply_date_to :申請日_まで
        application_form_code :申請書コード

    Returns:
        applicationInfoDtoList

    Raises:
        LaubeException : Laube例外
    """
    def get_application_list_count(self, session, company_code, target_company_code, target_group_code, target_employee_code, application_number_list, re_application_number, application_classification_code_list, application_status_list, apply_date_from, apply_date_to, application_form_code=None):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            application_list = applicationObjectDao.find_application_list(session, company_code, target_company_code, target_group_code, target_employee_code, application_number_list, re_application_number, application_classification_code_list, application_status_list, apply_date_from, apply_date_to, None, application_form_code)

            return len(application_list)

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    申請一覧画面のViewAPIにて呼び出される事を想定しています。
    申請状況画面のViewAPIにて呼び出される事を想定しています。

    [機能]
    申請一覧の取得を行います。
    申請状況の取得を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        target_company_code : 会社コード[対象者]
        target_group_code : 部署コード[対象者]
        target_employee_code : 従業員番号[対象者]
        application_number_list : 申請番号のリスト
        re_application_number : 再申請番号
        application_classification_code_list : 申請分類コードのリスト
        application_status_list : 申請書ステータスのリスト
        apply_date_from : 申請日_から
        apply_date_to :申請日_まで
        pagerDto: ページング
        application_form_code : 申請書コード

    Returns:
        applicationInfoDtoList

    Raises:
        LaubeException : Laube例外
    """
    def get_application_list(self, session, company_code, target_company_code, target_group_code, target_employee_code, application_number_list, re_application_number, application_classification_code_list, application_status_list, apply_date_from, apply_date_to, pagerDto, application_form_code=None):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if pagerDto is None:
                pagerDto = pagerDto()
                pagerDto.pagerCount = 1
                pagerDto.limit = 20
                pass

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            application_list = applicationObjectDao.find_application_list(session, company_code, target_company_code, target_group_code, target_employee_code, application_number_list, re_application_number, application_classification_code_list, application_status_list, apply_date_from, apply_date_to, pagerDto, application_form_code)
            applicationInfoDtoList = list()

            for application in application_list:
                applicationInfoDto = ApplicationInfoDto()

                is_apply_employee = company_code == application.ApplicationObject.target_company_code and target_employee_code == application.ApplicationObject.target_employee_code
                is_apply_employee = is_apply_employee or (company_code == application.ApplicationObject.applicant_company_code and target_employee_code == application.ApplicationObject.applicant_employee_code)

                # 申請者または対象者が本メソッドを実行した場合、[申請モード1]/[申請モード2]/[申請モード3]/[参照モード2]の何れかを判定します。
                if is_apply_employee:
                    applicationInfoDto.screen_mode = self._get_button_style(session, company_code, application.ApplicationObject.application_status, application.ApplicationObject.application_form_code)
                else:
                    applicationInfoDto.screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1　[ボタンなし]

                applicationInfoDto.application_number = application.ApplicationObject.application_number
                applicationInfoDto.re_application_number = application.ApplicationObject.re_application_number
                applicationInfoDto.application_classification_code = application.ApplicationClassification.application_classification_code
                applicationInfoDto.application_classification_name = application.ApplicationClassification.application_classification_name
                applicationInfoDto.application_form_code = application.ApplicationForm.application_form_code
                applicationInfoDto.application_form_name = application.ApplicationForm.application_form_name
                applicationInfoDto.application_status = application.ApplicationObject.application_status
                applicationInfoDto.applicant_status = None
                applicationInfoDto.apply_date = application.ApplicationObject.apply_date
                applicationInfoDto.target_company_code = application.ApplicationObject.target_company_code
                applicationInfoDto.target_company_name = self.__get_company_name(session, application.ApplicationObject.target_company_code)
                applicationInfoDto.target_group_code = application.ApplicationObject.target_group_code
                applicationInfoDto.target_group_name = self.__get_group_name(session, application.ApplicationObject.target_company_code, application.ApplicationObject.target_group_code)
                applicationInfoDto.target_employee_code = application.ApplicationObject.target_employee_code
                applicationInfoDto.target_employee_name = self.__get_employee_name(session, application.ApplicationObject.target_company_code, application.ApplicationObject.target_employee_code)
                applicationInfoDto.applicant_company_code = application.ApplicationObject.applicant_company_code
                applicationInfoDto.applicant_company_name = self.__get_company_name(session, application.ApplicationObject.applicant_company_code)
                applicationInfoDto.applicant_group_code = application.ApplicationObject.applicant_group_code
                applicationInfoDto.applicant_group_name = self.__get_group_name(session, application.ApplicationObject.applicant_company_code, application.ApplicationObject.applicant_group_code)
                applicationInfoDto.applicant_employee_code = application.ApplicationObject.applicant_employee_code
                applicationInfoDto.applicant_employee_name = self.__get_employee_name(session, application.ApplicationObject.applicant_company_code, application.ApplicationObject.applicant_employee_code)

                applicationInfoDto.approverl_list = list()

                # 申請書履歴オブジェクトより審査履歴を取得
                routeHistoryDao = RouteHistoryDao()
                route_history_list = routeHistoryDao.find_all_by_sort(session, application.ApplicationObject.target_company_code, application.ApplicationObject.application_number)

                for route_history in route_history_list:
                    approverlDataInfoDto = ApproverlDataInfoDto()
                    approverlDataInfoDto.company_code = route_history.company_code
                    approverlDataInfoDto.company_name = route_history.company_name
                    approverlDataInfoDto.application_number = route_history.application_number
                    approverlDataInfoDto.target_company_code = route_history.target_company_code  # 対象者の会社コード
                    approverlDataInfoDto.target_company_name = self.__get_company_name(session, route_history.target_company_code)  # 対象者の会社名
                    approverlDataInfoDto.target_group_code = route_history.target_group_code  # 対象者の部署コード
                    approverlDataInfoDto.target_group_name = self.__get_group_name(session, route_history.target_company_code, route_history.target_group_code)  # 対象者の部署名
                    approverlDataInfoDto.target_employee_code = route_history.target_employee_code  # 対象者の従業員番号
                    approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, route_history.target_company_code, route_history.target_employee_code)  # 対象者の従業員名
                    approverlDataInfoDto.applicant_company_code = route_history.applicant_company_code  # 申請者の会社コード
                    approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, route_history.applicant_company_code)  # 申請者の会社名
                    approverlDataInfoDto.applicant_group_code = route_history.applicant_group_code  # 申請者の部署コード
                    approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, route_history.applicant_company_code, route_history.applicant_group_code)  # 申請者の部署名
                    approverlDataInfoDto.applicant_employee_code = route_history.applicant_employee_code  # 申請者の従業員番号
                    approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, route_history.applicant_company_code, route_history.applicant_employee_code)  # 申請者の従業員名
                    approverlDataInfoDto.apply_date = route_history.apply_date  # 申請日
                    approverlDataInfoDto.application_status = route_history.application_status  # 申請書ステータス
                    approverlDataInfoDto.applicant_status = route_history.applicant_status  # 申請者ステータス
                    approverlDataInfoDto
                    approverlDataInfoDto.route_type = route_history.route_type
                    approverlDataInfoDto.route_number = route_history.route_number
                    approverlDataInfoDto.approverl_company_code = route_history.approverl_company_code
                    approverlDataInfoDto.approverl_company_name = route_history.approverl_company_name
                    approverlDataInfoDto.approverl_role_code = route_history.approverl_role_code
                    approverlDataInfoDto.approverl_role_name = route_history.approverl_role_name
                    approverlDataInfoDto.approverl_group_code = route_history.approverl_group_code
                    approverlDataInfoDto.approverl_group_name = route_history.approverl_group_name
                    approverlDataInfoDto.approverl_employee_code = route_history.approverl_employee_code
                    approverlDataInfoDto.approverl_employee_name = route_history.approverl_employee_name
                    approverlDataInfoDto.deputy_approverl_company_code = route_history.deputy_approverl_company_code
                    approverlDataInfoDto.deputy_approverl_company_name = route_history.deputy_approverl_company_name
                    approverlDataInfoDto.deputy_approverl_group_code = route_history.deputy_approverl_group_code
                    approverlDataInfoDto.deputy_approverl_group_name = route_history.deputy_approverl_group_name
                    approverlDataInfoDto.deputy_approverl_employee_code = route_history.deputy_approverl_employee_code
                    approverlDataInfoDto.deputy_approverl_employee_name = route_history.deputy_approverl_employee_name
                    approverlDataInfoDto.deputy_contents = route_history.deputy_contents
                    approverlDataInfoDto.approval_function = route_history.function
                    approverlDataInfoDto.reaching_date = route_history.reaching_date
                    approverlDataInfoDto.process_date = route_history.process_date
                    approverlDataInfoDto.activity_status = route_history.activity_status
                    approverlDataInfoDto.approverl_comment = route_history.approverl_comment

                    applicationInfoDto.approverl_list.append(approverlDataInfoDto)

                # 申請明細オブジェクトを検索します。
                activityObjectDao = ActivityObjectDao()
                activityObjects = activityObjectDao.find_by_company_code_application_number(session, application.ApplicationObject.target_company_code, application.ApplicationObject.application_number)

                for activityObject in activityObjects:

                    if activityObject.activity_status in [ActivityStatus.AUTHORIZER_UNTREATED, ActivityStatus.ARRIVAL, ActivityStatus.HOLD]:
                        approverlDataInfoDto = ApproverlDataInfoDto()
                        approverlDataInfoDto.company_code = activityObject.company_code
                        approverlDataInfoDto.company_name = self.__get_company_name(session, activityObject.company_code)
                        approverlDataInfoDto.application_number = activityObject.application_number
                        approverlDataInfoDto.target_company_code = application.ApplicationObject.target_company_code  # 対象者の会社コード
                        approverlDataInfoDto.target_company_name = self.__get_company_name(session, application.ApplicationObject.target_company_code)  # 対象者の会社名
                        approverlDataInfoDto.target_group_code = application.ApplicationObject.target_group_code  # 対象者の部署コード
                        approverlDataInfoDto.target_group_name = self.__get_group_name(session, application.ApplicationObject.target_company_code, application.ApplicationObject.target_group_code)  # 対象者の部署名
                        approverlDataInfoDto.target_employee_code = application.ApplicationObject.target_employee_code  # 対象者の従業員番号
                        approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, application.ApplicationObject.target_company_code, application.ApplicationObject.target_employee_code)  # 対象者の従業員名
                        approverlDataInfoDto.applicant_company_code = application.ApplicationObject.applicant_company_code  # 申請者の会社コード
                        approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, application.ApplicationObject.applicant_company_code)  # 申請者の会社名
                        approverlDataInfoDto.applicant_group_code = application.ApplicationObject.applicant_group_code  # 申請者の部署コード
                        approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, application.ApplicationObject.applicant_company_code, application.ApplicationObject.applicant_group_code)  # 申請者の部署名
                        approverlDataInfoDto.applicant_employee_code = application.ApplicationObject.applicant_employee_code  # 申請者の従業員番号
                        approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, application.ApplicationObject.applicant_company_code, application.ApplicationObject.applicant_employee_code)  # 申請者の従業員名
                        approverlDataInfoDto.apply_date = application.ApplicationObject.apply_date  # 申請日
                        approverlDataInfoDto.application_status = None  # 申請書ステータス
                        approverlDataInfoDto.applicant_status = None  # 申請者ステータス
                        approverlDataInfoDto.route_type = activityObject.route_type
                        approverlDataInfoDto.route_number = activityObject.route_number
                        approverlDataInfoDto.approverl_company_code = activityObject.approverl_company_code
                        approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, activityObject.approverl_company_code)

                        approverlDataInfoDto.approverl_role_code = activityObject.approverl_role_code

                        roleDao = RoleDao()
                        role = roleDao.find_ix_m_role(session, activityObject.approverl_company_code, activityObject.approverl_role_code)

                        if role is None:
                            approverlDataInfoDto.approverl_role_name = None
                        else:
                            approverlDataInfoDto.approverl_role_name = role.role_name

                        approverlDataInfoDto.approverl_group_code = activityObject.approverl_group_code
                        approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, activityObject.approverl_company_code, activityObject.approverl_group_code)
                        approverlDataInfoDto.approverl_employee_code = activityObject.approverl_employee_code
                        approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, activityObject.approverl_company_code, activityObject.approverl_employee_code)
                        approverlDataInfoDto.deputy_approverl_company_code = activityObject.deputy_approverl_company_code
                        approverlDataInfoDto.deputy_approverl_company_name = self.__get_company_name(session, activityObject.deputy_approverl_company_code)
                        approverlDataInfoDto.deputy_approverl_group_code = activityObject.deputy_approverl_group_code
                        approverlDataInfoDto.deputy_approverl_group_name = self.__get_group_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_group_code)
                        approverlDataInfoDto.deputy_approverl_employee_code = activityObject.deputy_approverl_employee_code
                        approverlDataInfoDto.deputy_approverl_employee_name = self.__get_employee_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_employee_code)
                        approverlDataInfoDto.deputy_contents = activityObject.deputy_contents
                        approverlDataInfoDto.approval_function = activityObject.function
                        approverlDataInfoDto.reaching_date = activityObject.reaching_date
                        approverlDataInfoDto.process_date = activityObject.process_date
                        approverlDataInfoDto.activity_status = activityObject.activity_status
                        approverlDataInfoDto.approverl_comment = activityObject.approverl_comment
                        applicationInfoDto.approverl_list.append(approverlDataInfoDto)

                applicationInfoDtoList.append(applicationInfoDto)

            return applicationInfoDtoList

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    下記のInitAPIにて呼び出される事を想定しています。
    ※申請者/対象者が呼び出した場合、下書き/申請/取り下げ/再申請も行える画面を返却します。
    申請画面のInitAPI
    申請一覧画面[詳細]のInitAPI

    [機能]
    申請番号にて申請書を取得します。

    Args:
        session: セッション情報
        company_code: 会社コード[ログイン]
        employee_code: 従業員番号[ログイン]
        target_company_code: 会社コード[対象者]
        application_number: 申請番号

    Returns:
        applicationInfoDto : 申請内容

    Raises:
        LaubeException : Laube例外
    """
    def find_apply(self, session, company_code, employee_code, target_company_code, application_number):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if not employee_code:
                raise LaubeException('required employee_code')

            if not target_company_code:
                raise LaubeException(self.E002)

            if application_number is None:
                raise LaubeException('required applicatrion_number')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, target_company_code, application_number)

            if applicationObject is None:
                raise LaubeException(f'applicationObject record is missing. key={target_company_code},{application_number}')

            is_apply_employee = company_code == applicationObject.target_company_code and employee_code == applicationObject.target_employee_code
            is_apply_employee = is_apply_employee or (company_code == applicationObject.applicant_company_code and employee_code == applicationObject.applicant_employee_code)

            applicationInfoDto = ApplicationInfoDto()

            # 申請者または対象者が本メソッドを実行した場合、[申請モード1]/[申請モード2]/[申請モード3]/[参照モード2]の何れかを判定します。
            if is_apply_employee:
                applicationInfoDto.screen_mode = self._get_button_style(session, company_code, applicationObject.application_status, applicationObject.application_form_code)
            else:
                applicationInfoDto.screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1　[ボタンなし]

            applicationInfoDto.application_number = applicationObject.application_number
            applicationInfoDto.re_application_number = applicationObject.re_application_number
            applicationInfoDto.application_form_code = applicationObject.application_form_code
            applicationInfoDto.application_form_name, applicationInfoDto.application_classification_code, applicationInfoDto.application_classification_name = self.__get_application_form_name(session, applicationObject.target_company_code, applicationObject.application_form_code)
            applicationInfoDto.target_company_code = applicationObject.target_company_code
            applicationInfoDto.target_company_name = self.__get_company_name(session, applicationObject.target_company_code)
            applicationInfoDto.target_group_code = applicationObject.target_group_code
            applicationInfoDto.target_group_name = self.__get_group_name(session, applicationObject.target_company_code, applicationObject.target_group_code)
            applicationInfoDto.target_employee_code = applicationObject.target_employee_code
            applicationInfoDto.target_employee_name = self.__get_employee_name(session, applicationObject.target_company_code, applicationObject.target_employee_code)
            applicationInfoDto.applicant_company_code = applicationObject.applicant_company_code
            applicationInfoDto.applicant_company_name = self.__get_company_name(session, applicationObject.applicant_company_code)
            applicationInfoDto.applicant_group_code = applicationObject.applicant_group_code
            applicationInfoDto.applicant_group_name = self.__get_group_name(session, applicationObject.applicant_company_code, applicationObject.applicant_group_code)
            applicationInfoDto.applicant_employee_code = applicationObject.applicant_employee_code
            applicationInfoDto.applicant_employee_name = self.__get_employee_name(session, applicationObject.applicant_company_code, applicationObject.applicant_employee_code)
            applicationInfoDto.apply_date = applicationObject.apply_date
            applicationInfoDto.application_status = applicationObject.application_status
            applicationInfoDto.applicant_status = None

            applicationInfoDto.approverl_list = list()  # 承認ルート

            # 申請書履歴オブジェクトより審査履歴を取得
            routeHistoryDao = RouteHistoryDao()
            route_history_list = routeHistoryDao.find_all_by_sort(session, applicationInfoDto.target_company_code, applicationInfoDto.application_number)

            for route_history in route_history_list:

                approverlDataInfoDto = ApproverlDataInfoDto()
                approverlDataInfoDto.company_code = route_history.company_code
                approverlDataInfoDto.company_name = route_history.company_name
                approverlDataInfoDto.application_number = route_history.application_number
                approverlDataInfoDto.target_company_code = route_history.target_company_code  # 対象者の会社コード
                approverlDataInfoDto.target_company_name = self.__get_company_name(session, route_history.target_company_code)  # 対象者の会社名
                approverlDataInfoDto.target_group_code = route_history.target_group_code  # 対象者の部署コード
                approverlDataInfoDto.target_group_name = self.__get_group_name(session, route_history.target_company_code, route_history.target_group_code)  # 対象者の部署名
                approverlDataInfoDto.target_employee_code = route_history.target_employee_code  # 対象者の従業員番号
                approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, route_history.target_company_code, route_history.target_employee_code)  # 対象者の従業員名
                approverlDataInfoDto.applicant_company_code = route_history.applicant_company_code  # 申請者の会社コード
                approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, route_history.applicant_company_code)  # 申請者の会社名
                approverlDataInfoDto.applicant_group_code = route_history.applicant_group_code  # 申請者の部署コード
                approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, route_history.applicant_company_code, route_history.applicant_group_code)  # 申請者の部署名
                approverlDataInfoDto.applicant_employee_code = route_history.applicant_employee_code  # 申請者の従業員番号
                approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, route_history.applicant_company_code, route_history.applicant_employee_code)  # 申請者の従業員名
                approverlDataInfoDto.apply_date = route_history.apply_date  # 申請日
                approverlDataInfoDto.application_status = route_history.application_status  # 申請書ステータス
                approverlDataInfoDto.applicant_status = route_history.applicant_status  # 申請者ステータス
                approverlDataInfoDto.route_type = route_history.route_type
                approverlDataInfoDto.route_number = route_history.route_number
                approverlDataInfoDto.approverl_company_code = route_history.approverl_company_code
                approverlDataInfoDto.approverl_company_name = route_history.approverl_company_name
                approverlDataInfoDto.approverl_role_code = route_history.approverl_role_code
                approverlDataInfoDto.approverl_role_name = route_history.approverl_role_name
                approverlDataInfoDto.approverl_group_code = route_history.approverl_group_code
                approverlDataInfoDto.approverl_group_name = route_history.approverl_group_name
                approverlDataInfoDto.approverl_employee_code = route_history.approverl_employee_code
                approverlDataInfoDto.approverl_employee_name = route_history.approverl_employee_name
                approverlDataInfoDto.deputy_approverl_company_code = route_history.deputy_approverl_company_code
                approverlDataInfoDto.deputy_approverl_company_name = route_history.deputy_approverl_company_name
                approverlDataInfoDto.deputy_approverl_group_code = route_history.deputy_approverl_group_code
                approverlDataInfoDto.deputy_approverl_group_name = route_history.deputy_approverl_group_name
                approverlDataInfoDto.deputy_approverl_employee_code = route_history.deputy_approverl_employee_code
                approverlDataInfoDto.deputy_approverl_employee_name = route_history.deputy_approverl_employee_name
                approverlDataInfoDto.deputy_contents = route_history.deputy_contents
                approverlDataInfoDto.approval_function = route_history.function
                approverlDataInfoDto.reaching_date = route_history.reaching_date
                approverlDataInfoDto.process_date = route_history.process_date
                approverlDataInfoDto.activity_status = route_history.activity_status
                approverlDataInfoDto.approverl_comment = route_history.approverl_comment
                applicationInfoDto.route_history_list.append(approverlDataInfoDto)

            # 申請明細オブジェクトを検索します。
            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, applicationObject.target_company_code, application_number)

            for activityObject in activityObjects:

                approverlDataInfoDto = ApproverlDataInfoDto()
                approverlDataInfoDto.company_code = activityObject.company_code
                approverlDataInfoDto.company_name = self.__get_company_name(session, activityObject.company_code)
                approverlDataInfoDto.application_number = activityObject.application_number
                approverlDataInfoDto.target_company_code = applicationObject.target_company_code  # 対象者の会社コード
                approverlDataInfoDto.target_company_name = self.__get_company_name(session, applicationObject.target_company_code)  # 対象者の会社名
                approverlDataInfoDto.target_group_code = applicationObject.target_group_code  # 対象者の部署コード
                approverlDataInfoDto.target_group_name = self.__get_group_name(session, applicationObject.target_company_code, applicationObject.target_group_code)  # 対象者の部署名
                approverlDataInfoDto.target_employee_code = applicationObject.target_employee_code  # 対象者の従業員番号
                approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, applicationObject.target_company_code, applicationObject.target_employee_code)  # 対象者の従業員名
                approverlDataInfoDto.applicant_company_code = applicationObject.applicant_company_code  # 申請者の会社コード
                approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, applicationObject.applicant_company_code)  # 申請者の会社名
                approverlDataInfoDto.applicant_group_code = applicationObject.applicant_group_code  # 申請者の部署コード
                approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, applicationObject.applicant_company_code, applicationObject.applicant_group_code)  # 申請者の部署名
                approverlDataInfoDto.applicant_employee_code = applicationObject.applicant_employee_code  # 申請者の従業員番号
                approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, applicationObject.applicant_company_code, applicationObject.applicant_employee_code)  # 申請者の従業員名
                approverlDataInfoDto.apply_date = applicationObject.apply_date  # 申請日
                approverlDataInfoDto.application_status = applicationObject.application_status  # 申請書ステータス
                approverlDataInfoDto.applicant_status = None  # 申請者ステータス
                approverlDataInfoDto.route_type = activityObject.route_type
                approverlDataInfoDto.route_number = activityObject.route_number
                approverlDataInfoDto.approverl_company_code = activityObject.approverl_company_code
                approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, activityObject.approverl_company_code)

                approverlDataInfoDto.approverl_role_code = activityObject.approverl_role_code

                roleDao = RoleDao()
                role = roleDao.find_ix_m_role(session, activityObject.approverl_company_code, activityObject.approverl_role_code)

                if role is None:
                    approverlDataInfoDto.approverl_role_name = None
                else:
                    approverlDataInfoDto.approverl_role_name = role.role_name

                approverlDataInfoDto.approverl_group_code = activityObject.approverl_group_code
                approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, activityObject.approverl_company_code, activityObject.approverl_group_code)
                approverlDataInfoDto.approverl_employee_code = activityObject.approverl_employee_code
                approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, activityObject.approverl_company_code, activityObject.approverl_employee_code)
                approverlDataInfoDto.deputy_approverl_company_code = activityObject.deputy_approverl_company_code
                approverlDataInfoDto.deputy_approverl_company_name = self.__get_company_name(session, activityObject.deputy_approverl_company_code)
                approverlDataInfoDto.deputy_approverl_group_code = activityObject.deputy_approverl_group_code
                approverlDataInfoDto.deputy_approverl_group_name = self.__get_group_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_group_code)
                approverlDataInfoDto.deputy_approverl_employee_code = activityObject.deputy_approverl_employee_code
                approverlDataInfoDto.deputy_approverl_employee_name = self.__get_employee_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_employee_code)
                approverlDataInfoDto.deputy_contents = activityObject.deputy_contents
                approverlDataInfoDto.approval_function = activityObject.function
                approverlDataInfoDto.reaching_date = activityObject.reaching_date
                approverlDataInfoDto.process_date = activityObject.process_date
                approverlDataInfoDto.activity_status = activityObject.activity_status
                approverlDataInfoDto.approverl_comment = activityObject.approverl_comment
                applicationInfoDto.approverl_list.append(approverlDataInfoDto)

            return applicationInfoDto

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    申請者の利用可能ボタンを返却します。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_status : 申請書ステータス
        application_form_code : 申請書コード

    Returns:
        screen_mode

    Raises:
        LaubeException : Laube例外
    """
    def _get_button_style(self, session, company_code, application_status, application_form_code):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if application_status is None:
                raise LaubeException('required application_status')

            if application_form_code is None:
                raise LaubeException('required application_form_code')

            _screen_mode = None

            applicationFormDao = ApplicationFormDao()
            applicationForm = applicationFormDao.find_ix_m_application_form(session, company_code, application_form_code)

            if applicationForm is None:
                raise LaubeException(self.E006)

            match application_status:

                case ApplicationStatus.DRAFT:  # 現在、申請書は[下書き]状態
                    _screen_mode = ScreenMode.APPLY_MODE_2  # 申請モード2　[取り下げ/下書き/申請]
                    pass

                case ApplicationStatus.PULL_BACK:  # 現在、申請書は[引き戻し]状態
                    _screen_mode = ScreenMode.APPLY_MODE_3  # 申請モード3　[取り下げ/申請]
                    pass

                case ApplicationStatus.WITH_DRAWAL:  # 現在、申請書は[差し戻し]状態
                    _screen_mode = ScreenMode.APPLY_MODE_3  # 申請モード3　[取り下げ/申請]
                    pass

                case ApplicationStatus.UNDER_EXAMINATION:  # 現在、申請書は[審査中]状態

                    match applicationForm.pulling_flag:

                        case PullingFlag.NO_PULLING:  # [引き戻し禁止]に設定されている場合
                            _screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1　[ボタンなし]
                            pass

                        case PullingFlag.POSSIBLE_BEFORE_APPROVAL:  # [最終承認前なら可能]に設定されている場合
                            _screen_mode = ScreenMode.SEE_MODE_8  # 参照モード3　[引き戻し]
                            pass

                        case PullingFlag.POSSIBLE_AFTER_APPROVAL:  # [最終承認後も可能]に設定されている場合
                            _screen_mode = ScreenMode.SEE_MODE_8  # 参照モード3　[引き戻し]
                            pass

                case ApplicationStatus.DENIAL:  # 現在、申請書は[否認]状態

                    match applicationForm.pulling_flag:

                        case PullingFlag.NO_PULLING:  # [引き戻し禁止]に設定されている場合
                            _screen_mode = ScreenMode.SEE_MODE_2  # 参照モード2　[再申請]
                            pass

                        case PullingFlag.POSSIBLE_BEFORE_APPROVAL:  # [最終承認前なら可能]に設定されている場合
                            _screen_mode = ScreenMode.SEE_MODE_2  # 参照モード2　[再申請]

                            pass

                        case PullingFlag.POSSIBLE_AFTER_APPROVAL:  # [最終承認後も可能]に設定されている場合
                            _screen_mode = ScreenMode.SEE_MODE_3  # 参照モード2　[引き戻し][再申請]

                            pass

                case ApplicationStatus.APPROVED:  # 現在、申請書は[承認]状態

                    match applicationForm.pulling_flag:

                        case PullingFlag.NO_PULLING:  # [引き戻し禁止]に設定されている場合
                            _screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1　[ボタンなし]

                            pass

                        case PullingFlag.POSSIBLE_BEFORE_APPROVAL:  # [[最終承認前なら可能]に設定されている場合
                            _screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1　[ボタンなし]

                            pass

                        case PullingFlag.POSSIBLE_AFTER_APPROVAL:  # [[最終承認後も可能]に設定されている場合
                            _screen_mode = ScreenMode.SEE_MODE_8  # 参照モード3　[引き戻し]

                            pass

                case ApplicationStatus.CANCEL:  # 現在、申請書は[取り下げ]状態
                    _screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1　[ボタンなし]
                    pass

                case _:
                    raise LaubeException('error application_status')

            return _screen_mode

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    """
    [利用場所]
    申請番号を新規で割り当てる際、呼び出される事を想定しています。

    [機能]
    指定会社の申請書番号最大値を取得します。

    Args:
        session: セッション情報
        company_code: 会社コード

    Returns:
        application_number : 申請番号

    Raises:
        LaubeException : Laube例外
    """
    def __get_max_application_number(self, session, company_code):

        applicationObjectDao = ApplicationObjectDao()
        applicationObject = applicationObjectDao.find_max_application_number(session, company_code)
        if applicationObject is None:
            application_number = 0
        else:
            application_number = applicationObject.application_number
        return application_number

    """
    [利用場所]
    申請画面の下書きボタン押下時

    [機能]
    下書き処理を行います。

    [制約]
    applicationInfoDto.approverl_listは、必ず、直接部門ルートのルート番号の昇順　+ 間接部門ルートのルート番号の昇順でソートして下さい。

    Args:
        session: セッション情報
        applicationInfoDto: 申請内容

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def draft(self, session, applicationInfoDto):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not isinstance(applicationInfoDto, ApplicationInfoDto):
                raise LaubeException('required applicationInfoDto')

            screen_mode = applicationInfoDto.screen_mode

            # [下書き]以外はエラー
            if ((screen_mode != ScreenMode.APPLY_MODE_1) and (screen_mode != ScreenMode.APPLY_MODE_2)):
                raise LaubeException('unmatch screen_mode')

            application_number = applicationInfoDto.application_number

            # if applicationInfoDto.re_application_number is None:
            #     applicationInfoDto.re_application_number = ''
            re_application_number = applicationInfoDto.re_application_number
            application_form_code = applicationInfoDto.application_form_code
            if not application_form_code:
                raise LaubeException(self.E005)

            application_classification_code = applicationInfoDto.application_classification_code
            if not application_classification_code:
                raise LaubeException('required application_classification_code')

            target_company_code = applicationInfoDto.target_company_code
            if not target_company_code:
                raise LaubeException(self.E002)

            target_group_code = applicationInfoDto.target_group_code
            if not target_group_code:
                raise LaubeException(self.E003)

            target_employee_code = applicationInfoDto.target_employee_code
            if not target_employee_code:
                raise LaubeException(self.E004)

            applicant_company_code = applicationInfoDto.applicant_company_code
            if not applicant_company_code:
                raise LaubeException(self.E008)

            applicant_group_code = applicationInfoDto.applicant_group_code
            if not applicant_group_code:
                raise LaubeException(self.E009)

            applicant_employee_code = applicationInfoDto.applicant_employee_code
            if not applicant_employee_code:
                raise LaubeException(self.E010)

            # 承認ルートを確認します

            approverl_list = applicationInfoDto.approverl_list
            if approverl_list is None:
                raise LaubeException('required approverl_list')

            for approverlDataInfoDto in approverl_list:

                if approverlDataInfoDto.company_code is None or len(approverlDataInfoDto.company_code.strip()) == 0:
                    raise LaubeException('required company_code')

                if approverlDataInfoDto.route_type != RouteType.INDIVIDUAL_ROUTE and approverlDataInfoDto.route_type != RouteType.COMMON_ROUTE:
                    raise LaubeException('required route_type')

                if approverlDataInfoDto.route_number < 1:
                    raise LaubeException('required route_number')

                if approverlDataInfoDto.approverl_company_code is None or len(approverlDataInfoDto.approverl_company_code.strip()) == 0:
                    raise LaubeException('required approverl_company_code')

                check1 = approverlDataInfoDto.approverl_role_code is None or len(approverlDataInfoDto.approverl_role_code.strip()) == 0
                check2 = approverlDataInfoDto.approverl_group_code is None or len(approverlDataInfoDto.approverl_group_code.strip()) == 0
                check3 = approverlDataInfoDto.approverl_employee_code is None or len(approverlDataInfoDto.approverl_employee_code.strip()) == 0

                if check1 and check2 and check3:
                    raise LaubeException('required approverl_role_code')

                if check1 and (check2 and not check3):
                    raise LaubeException('required approverl_group_code')

                if check1 and (not check2 and check3):
                    raise LaubeException('required approverl_employee_code')

                check4 = approverlDataInfoDto.deputy_approverl_company_code is None or len(approverlDataInfoDto.deputy_approverl_company_code.strip()) == 0
                check5 = approverlDataInfoDto.deputy_approverl_group_code is None or len(approverlDataInfoDto.deputy_approverl_group_code.strip()) == 0
                check6 = approverlDataInfoDto.deputy_approverl_employee_code is None or len(approverlDataInfoDto.deputy_approverl_employee_code.strip()) == 0

                if check4 or check5 or check6:
                    if not check4 and not check5 and not check6:
                        raise LaubeException('required deputy_contents')

                if approverlDataInfoDto.approval_function != ApprovalFunction.EXAMINATION and approverlDataInfoDto.approval_function != ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL and approverlDataInfoDto.approval_function != ApprovalFunction.FUNCTION_CONFIRMATION and approverlDataInfoDto.approval_function != ApprovalFunction.AUTHORIZER_FORCED_APPROVAL:
                    raise LaubeException('required approval_function')

            dt = datetime.now()
            applicationObject = None

            # 申請がすでにされていないか確認します
            applicationObjectDao = ApplicationObjectDao()
            if application_number is not None and application_number > 0:
                applicationObject = applicationObjectDao.find_ix_t_application_object(session, target_company_code, application_number)
                # レコードが存在しているのに申請書ステータスが[下書き]でない場合は、エラー
                if applicationObject is not None and applicationObject.application_status != ApplicationStatus.DRAFT:
                    raise LaubeException('Application cannot be overwritten.')
                else:
                    # 申請明細オブジェクトを一旦削除します。
                    activityObjectDao = ActivityObjectDao()
                    activityObjectDao.delete_by_company_code_application_object(session, target_company_code, application_number)

                    # 申請オブジェクトを設定します
                    applicationObject = ApplicationObject()
                    applicationObject.company_code = target_company_code
                    applicationObject.application_number = application_number
                    applicationObject.re_application_number = re_application_number
                    applicationObject.application_form_code = application_form_code
                    applicationObject.target_company_code = target_company_code
                    applicationObject.target_group_code = target_group_code
                    applicationObject.target_employee_code = target_employee_code
                    applicationObject.applicant_company_code = applicant_company_code
                    applicationObject.applicant_group_code = applicant_group_code
                    applicationObject.applicant_employee_code = applicant_employee_code
                    applicationObject.apply_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                    applicationObject.application_status = ApplicationStatus.DRAFT  # 申請書ステータスを[下書き]に変更
                    applicationObject.create_employee_code = applicationObject.applicant_employee_code
                    applicationObject.update_employee_code = applicationObject.applicant_employee_code

            else:
                application_number = self.__get_max_application_number(session, target_company_code) + 1  # 申請番号を採番します。
                # 申請オブジェクトを設定します
                applicationObject = ApplicationObject()
                applicationObject.company_code = target_company_code
                applicationObject.application_number = application_number
                applicationObject.re_application_number = re_application_number
                applicationObject.application_form_code = application_form_code
                applicationObject.target_company_code = target_company_code
                applicationObject.target_group_code = target_group_code
                applicationObject.target_employee_code = target_employee_code
                applicationObject.applicant_company_code = applicant_company_code
                applicationObject.applicant_group_code = applicant_group_code
                applicationObject.applicant_employee_code = applicant_employee_code
                applicationObject.apply_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                applicationObject.application_status = ApplicationStatus.DRAFT  # 申請書ステータスを[下書き]に変更
                applicationObject.create_employee_code = applicationObject.applicant_employee_code
                applicationObject.update_employee_code = applicationObject.applicant_employee_code
                applicationObjectDao.add(session, applicationObject)

            # 申請明細オブジェクトを作成します。
            activityObjectDao = ActivityObjectDao()
            for approverlDataInfoDto in approverl_list:
                activityObject = ActivityObject()
                activityObject.company_code = target_company_code
                activityObject.application_number = application_number
                activityObject.route_type = approverlDataInfoDto.route_type
                activityObject.route_number = approverlDataInfoDto.route_number
                activityObject.approverl_company_code = approverlDataInfoDto.approverl_company_code
                activityObject.approverl_role_code = approverlDataInfoDto.approverl_role_code
                activityObject.approverl_group_code = approverlDataInfoDto.approverl_group_code
                activityObject.approverl_employee_code = approverlDataInfoDto.approverl_employee_code
                activityObject.deputy_approverl_company_code = approverlDataInfoDto.deputy_approverl_company_code
                activityObject.deputy_approverl_group_code = approverlDataInfoDto.deputy_approverl_group_code
                activityObject.deputy_approverl_employee_code = approverlDataInfoDto.deputy_approverl_employee_code
                activityObject.deputy_contents = approverlDataInfoDto.deputy_contents
                activityObject.function = approverlDataInfoDto.approval_function
                activityObject.reaching_date = approverlDataInfoDto.reaching_date
                activityObject.process_date = approverlDataInfoDto.process_date
                activityObject.activity_status = approverlDataInfoDto.activity_status
                activityObject.approverl_comment = approverlDataInfoDto.approverl_comment
                activityObject.create_employee_code = applicationObject.applicant_employee_code
                activityObject.update_employee_code = applicationObject.applicant_employee_code

                activityObject.update_count = 1
                activityObjectDao.add(session, activityObject)

            return application_number

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    申請画面の申請ボタン押下時

    [機能]
    申請処理を行います。

    [制約]
    applicationInfoDto.approverl_listは、必ず、直接部門ルートのルート番号の昇順　+ 間接部門ルートのルート番号の昇順でソートして下さい。

    Args:
        session : セッション情報
        applicationInfoDto : 申請内容

    Returns:
        application_number

    Raises:
        LaubeException : Laube例外
    """
    def apply(self, session, applicationInfoDto):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not isinstance(applicationInfoDto, ApplicationInfoDto):
                raise LaubeException('required applicationInfoDto')

            screen_mode = applicationInfoDto.screen_mode

            # [申請]以外はエラー
            if ((screen_mode != ScreenMode.APPLY_MODE_1) and (screen_mode != ScreenMode.APPLY_MODE_2) and (screen_mode != ScreenMode.APPLY_MODE_3) and (screen_mode != ScreenMode.SEE_MODE_2) and (screen_mode != ScreenMode.SEE_MODE_3) and (screen_mode != ScreenMode.SEE_MODE_4) and (screen_mode != ScreenMode.SEE_MODE_6)):
                raise LaubeException('unmatch screen_mode')

            application_number = applicationInfoDto.application_number
            # if applicationInfoDto.re_application_number is None:
            #     applicationInfoDto.re_application_number = ''
            re_application_number = applicationInfoDto.re_application_number
            application_form_code = applicationInfoDto.application_form_code
            if not application_form_code:
                raise LaubeException(self.E005)

            application_classification_code = applicationInfoDto.application_classification_code
            if not application_classification_code:
                raise LaubeException('required application_classification_code')

            target_company_code = applicationInfoDto.target_company_code
            if not target_company_code:
                raise LaubeException(self.E002)

            target_group_code = applicationInfoDto.target_group_code
            if not target_group_code:
                raise LaubeException(self.E003)

            target_employee_code = applicationInfoDto.target_employee_code
            if not target_employee_code:
                raise LaubeException(self.E004)

            applicant_company_code = applicationInfoDto.applicant_company_code
            if not applicant_company_code:
                raise LaubeException(self.E008)

            applicant_group_code = applicationInfoDto.applicant_group_code
            if not applicant_group_code:
                raise LaubeException(self.E009)

            applicant_employee_code = applicationInfoDto.applicant_employee_code
            if not applicant_employee_code:
                raise LaubeException(self.E010)

            # 承認ルートを確認します

            approverl_list = applicationInfoDto.approverl_list
            if approverl_list is None:
                raise LaubeException('required approverl_list')

            for approverlDataInfoDto in approverl_list:

                if approverlDataInfoDto.company_code is None or len(approverlDataInfoDto.company_code.strip()) == 0:
                    raise LaubeException('required company_code')

                if approverlDataInfoDto.route_type not in [RouteType.INDIVIDUAL_ROUTE, RouteType.COMMON_ROUTE]:
                    raise LaubeException('required route_type')

                if approverlDataInfoDto.route_number < 1:
                    raise LaubeException('required route_number')

                if approverlDataInfoDto.approverl_company_code is None or len(approverlDataInfoDto.approverl_company_code.strip()) == 0:
                    raise LaubeException('required approverl_company_code')

                check1 = approverlDataInfoDto.approverl_role_code is None or len(approverlDataInfoDto.approverl_role_code.strip()) == 0
                check2 = approverlDataInfoDto.approverl_group_code is None or len(approverlDataInfoDto.approverl_group_code.strip()) == 0
                check3 = approverlDataInfoDto.approverl_employee_code is None or len(approverlDataInfoDto.approverl_employee_code.strip()) == 0

                if check1 and check2 and check3:
                    raise LaubeException('required approverl_role_code')

                if check1 and (check2 and not check3):
                    raise LaubeException('required approverl_group_code')

                if check1 and (not check2 and check3):
                    raise LaubeException('required approverl_employee_code')

                check4 = approverlDataInfoDto.deputy_approverl_company_code is None or len(approverlDataInfoDto.deputy_approverl_company_code.strip()) == 0
                check5 = approverlDataInfoDto.deputy_approverl_group_code is None or len(approverlDataInfoDto.deputy_approverl_group_code.strip()) == 0
                check6 = approverlDataInfoDto.deputy_approverl_employee_code is None or len(approverlDataInfoDto.deputy_approverl_employee_code.strip()) == 0

                if check4 or check5 or check6:
                    if not check4 and not check5 and not check6:
                        raise LaubeException('required deputy_contents')

                if approverlDataInfoDto.approval_function != ApprovalFunction.EXAMINATION and approverlDataInfoDto.approval_function != ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL and approverlDataInfoDto.approval_function != ApprovalFunction.FUNCTION_CONFIRMATION and approverlDataInfoDto.approval_function != ApprovalFunction.AUTHORIZER_FORCED_APPROVAL:
                    raise LaubeException('required approval_function')

            dt = datetime.now()
            applicationObject = None

            # 申請がすでにされていないか確認します
            applicationObjectDao = ApplicationObjectDao()
            if application_number is not None and application_number > 0:
                applicationObject = applicationObjectDao.find_ix_t_application_object(session, target_company_code, application_number)
                # レコードが存在しているのに申請書ステータスが[下書き][引き戻し][差し戻し]でない場合は、エラー
                if applicationObject and applicationObject.application_status not in [ApplicationStatus.DRAFT, ApplicationStatus.PULL_BACK, ApplicationStatus.WITH_DRAWAL]:
                    raise LaubeException('Application cannot be overwritten.')
                else:
                    # 申請明細オブジェクトを一旦削除します。
                    activityObjectDao = ActivityObjectDao()
                    activityObjectDao.delete_by_company_code_application_object(session, target_company_code, application_number)

                    # 申請オブジェクトを設定します
                    applicationObject.company_code = target_company_code
                    applicationObject.application_number = application_number
                    applicationObject.re_application_number = re_application_number
                    applicationObject.application_form_code = application_form_code
                    applicationObject.target_company_code = target_company_code
                    applicationObject.target_group_code = target_group_code
                    applicationObject.target_employee_code = target_employee_code
                    applicationObject.applicant_company_code = applicant_company_code
                    applicationObject.applicant_group_code = applicant_group_code
                    applicationObject.applicant_employee_code = applicant_employee_code
                    applicationObject.apply_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                    applicationObject.application_status = ApplicationStatus.UNDER_EXAMINATION  # 申請書ステータスを[審査中]に変更
                    applicationObject.create_employee_code = applicationObject.applicant_employee_code
                    applicationObject.update_employee_code = applicationObject.applicant_employee_code

            else:
                # 申請オブジェクトを設定します
                applicationObject = ApplicationObject()
                applicationObject.company_code = target_company_code
                application_number = self.__get_max_application_number(session, target_company_code) + 1  # 申請番号を採番します。
                applicationObject.application_number = application_number
                applicationObject.re_application_number = re_application_number
                applicationObject.application_form_code = application_form_code
                applicationObject.target_company_code = target_company_code
                applicationObject.target_group_code = target_group_code
                applicationObject.target_employee_code = target_employee_code
                applicationObject.applicant_company_code = applicant_company_code
                applicationObject.applicant_group_code = applicant_group_code
                applicationObject.applicant_employee_code = applicant_employee_code
                applicationObject.apply_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                applicationObject.application_status = ApplicationStatus.UNDER_EXAMINATION  # 申請書ステータスを[審査中]に変更
                applicationObject.create_employee_code = applicationObject.applicant_employee_code
                applicationObject.update_employee_code = applicationObject.applicant_employee_code
                applicationObjectDao.add(session, applicationObject)

            # 申請明細オブジェクトを作成します。(承認者ステータスを[到着]にするのはあとで行います。)
            activityObjectDao = ActivityObjectDao()
            for approverlDataInfoDto in approverl_list:
                activityObject = ActivityObject()
                activityObject.company_code = target_company_code
                activityObject.application_number = application_number
                activityObject.route_type = approverlDataInfoDto.route_type
                activityObject.route_number = approverlDataInfoDto.route_number
                activityObject.approverl_company_code = approverlDataInfoDto.approverl_company_code
                activityObject.approverl_role_code = approverlDataInfoDto.approverl_role_code
                activityObject.approverl_group_code = approverlDataInfoDto.approverl_group_code
                activityObject.approverl_employee_code = approverlDataInfoDto.approverl_employee_code
                activityObject.deputy_approverl_company_code = approverlDataInfoDto.deputy_approverl_company_code
                activityObject.deputy_approverl_group_code = approverlDataInfoDto.deputy_approverl_group_code
                activityObject.deputy_approverl_employee_code = approverlDataInfoDto.deputy_approverl_employee_code
                activityObject.deputy_contents = approverlDataInfoDto.deputy_contents
                activityObject.function = approverlDataInfoDto.approval_function
                activityObject.reaching_date = approverlDataInfoDto.reaching_date
                activityObject.process_date = approverlDataInfoDto.process_date
                activityObject.activity_status = approverlDataInfoDto.activity_status
                activityObject.approverl_comment = approverlDataInfoDto.approverl_comment
                activityObject.create_employee_code = applicationObject.applicant_employee_code
                activityObject.update_employee_code = applicationObject.applicant_employee_code

                activityObject.update_count = 1
                activityObjectDao.add(session, activityObject)

            # 申請書履歴オブジェクトに追加します
            self.__add_history(session, applicationObject, None, ApplicantStatus.APPLY)

            session.flush()

            # 申請明細オブジェクトを再検索します。
            activityObjectDao = ActivityObjectDao()
            activityObject_list = activityObjectDao.find_by_company_code_application_number(session, target_company_code, application_number)

            # 申請後、最初に到着する承認者の承認者ステータスを[到着]に更新します。
            present_route_type = 0
            present_route_number = 0
            is_finish = True

            for activityObject in activityObject_list:

                if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED:  # 未処理

                    if present_route_number == 0 or (present_route_type == activityObject.route_type and present_route_number == activityObject.route_number):  # 最初の承認者または同一のルート番号の場合(並列)

                        if activityObject.function == ApprovalFunction.EXAMINATION:  # [承認画面の機能]が[審査]
                            activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                            activityObject.process_date = None  # 処理日
                            activityObject.activity_status = ActivityStatus.ARRIVAL  # 到着
                            activityObject.approverl_comment = None  # 承認者のコメント
                            present_route_type = activityObject.route_type  # ルートタイプ
                            present_route_number = activityObject.route_number  # ルート番号
                            is_finish = False

                        else:
                            if activityObject.function == ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL:  # [承認画面の機能]が[自動承認]
                                activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                                activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日
                                activityObject.activity_status = ActivityStatus.AUTHORIZER_AUTOMATIC_APPROVAL  # 自動承認
                                activityObject.approverl_comment = '自動承認されました。'  # 承認者のコメント
                                present_route_type = 0  # ルートタイプ
                                present_route_number = 0  # ルート番号

                                # 申請書履歴オブジェクトに追加します
                                self.__add_history(session, applicationObject, activityObject, None)

                            else:
                                if activityObject.function == ApprovalFunction.FUNCTION_CONFIRMATION:  # [承認画面の機能]が[確認]
                                    activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                                    activityObject.process_date = None  # 処理日
                                    activityObject.activity_status = ActivityStatus.ARRIVAL  # 到着
                                    activityObject.approverl_comment = None  # 承認者のコメント
                                    present_route_type = activityObject.route_type  # ルートタイプ
                                    present_route_number = activityObject.route_number  # ルート番号
                                    is_finish = False

                                else:
                                    raise LaubeException('function is missing.')
                    else:
                        break

                else:
                    break

            if is_finish:
                session.flush()
                applicationObject = applicationObjectDao.find_ix_t_application_object(session, target_company_code, application_number)
                activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                activityObject.activity_status = ActivityStatus.AUTHORIZER_AUTOMATIC_APPROVAL  # 自動承認
                activityObject.approverl_comment = '自動承認されました。'  # 承認者のコメント
                applicationObject.application_status = ApplicationStatus.APPROVED  # 申請書ステータスを[承認]に変更
                applicationObject.approval_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 承認日

                # 申請書履歴オブジェクトに追加します
                self.__add_history(session, applicationObject, activityObject, None)

            return application_number

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    詳細画面の引き戻しボタン押下時

    [機能]
    引き戻し処理を行います。

    [制約]
    applicationInfoDto.approverl_listは、必ず、直接部門ルートのルート番号の昇順　+ 間接部門ルートのルート番号の昇順でソートして下さい。

    Args:
        session : セッション情報
        applicationInfoDto : 申請内容

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def pull_back(self, session, applicationInfoDto):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not isinstance(applicationInfoDto, ApplicationInfoDto):
                raise LaubeException('required applicationInfoDto')

            screen_mode = applicationInfoDto.screen_mode

            # [引き戻し]以外はエラー
            if screen_mode != ScreenMode.SEE_MODE_3 and screen_mode != ScreenMode.SEE_MODE_5 and screen_mode != ScreenMode.SEE_MODE_6 and screen_mode != ScreenMode.SEE_MODE_8:
                raise LaubeException('unmatch screen_mode')

            application_number = applicationInfoDto.application_number

            if application_number is None:
                raise LaubeException('required application_number')

            re_application_number = applicationInfoDto.re_application_number
            application_form_code = applicationInfoDto.application_form_code
            if not application_form_code:
                raise LaubeException(self.E005)

            application_classification_code = applicationInfoDto.application_classification_code
            if not application_classification_code:
                raise LaubeException('required application_classification_code')

            target_company_code = applicationInfoDto.target_company_code
            if not target_company_code:
                raise LaubeException(self.E002)

            target_group_code = applicationInfoDto.target_group_code
            if not target_group_code:
                raise LaubeException(self.E003)

            target_employee_code = applicationInfoDto.target_employee_code
            if not target_employee_code:
                raise LaubeException(self.E004)

            applicant_company_code = applicationInfoDto.applicant_company_code
            if not applicant_company_code:
                raise LaubeException(self.E008)

            applicant_group_code = applicationInfoDto.applicant_group_code
            if not applicant_group_code:
                raise LaubeException(self.E009)

            applicant_employee_code = applicationInfoDto.applicant_employee_code
            if not applicant_employee_code:
                raise LaubeException(self.E010)

            apply_date = applicationInfoDto.apply_date
            if apply_date is None:
                raise LaubeException('required apply_date')

            dt = datetime.now()
            applicationObject = None
            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, target_company_code, application_number)
            # 申請書ステータスが[取り下げ]の場合は、エラー
            if applicationObject is not None and (applicationObject.application_status == ApplicationStatus.CANCEL):
                raise LaubeException('Application cannot be overwritten.')
            else:
                # 申請オブジェクトを設定します
                applicationObject.company_code = target_company_code
                applicationObject.application_number = application_number
                applicationObject.re_application_number = re_application_number
                applicationObject.application_form_code = application_form_code
                applicationObject.target_company_code = target_company_code
                applicationObject.target_group_code = target_group_code
                applicationObject.target_employee_code = target_employee_code
                applicationObject.applicant_company_code = applicant_company_code
                applicationObject.applicant_group_code = applicant_group_code
                applicationObject.applicant_employee_code = applicant_employee_code
                applicationObject.apply_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                applicationObject.application_status = ApplicationStatus.PULL_BACK  # 申請書ステータスを[引き戻し]に変更
                applicationObject.update_employee_code = applicationObject.applicant_employee_code
                # 申請書履歴オブジェクトに追加します
                self.__add_history(session, applicationObject, None, ApplicantStatus.PULL_BACK)

            # 申請明細オブジェクトを再検索します。
            activityObjectDao = ActivityObjectDao()
            activityObject_list = activityObjectDao.find_by_company_code_application_number(session, target_company_code, application_number)

            # 全ての承認者の承認情報を初期化します。
            for activityObject in activityObject_list:
                activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED  # [未処理]
                activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                activityObject.process_date = None  # 処理日
                activityObject.activity_status = ActivityStatus.AUTHORIZER_UNTREATED  # 未処理
                activityObject.approverl_comment = None  # 承認者のコメント

            return True

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    申請画面の取り下げボタン押下時

    [機能]
    取り下げ処理を行います。

    [制約]
    applicationInfoDto.approverl_listは、必ず、直接部門ルートのルート番号の昇順　+ 間接部門ルートのルート番号の昇順でソートして下さい。

    Args:
        session : セッション情報
        applicationInfoDto : 申請内容

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def cancel(self, session, applicationInfoDto):

        try:
            if not session:
                raise LaubeException(self.E001)

            # 引数を確認します
            if not isinstance(applicationInfoDto, ApplicationInfoDto):
                raise LaubeException('required applicationInfoDto')

            screen_mode = applicationInfoDto.screen_mode

            # [取り下げ]以外はエラー
            if ((screen_mode != ScreenMode.APPLY_MODE_2) and (screen_mode != ScreenMode.APPLY_MODE_3) and (screen_mode != ScreenMode.SEE_MODE_4) and (screen_mode != ScreenMode.SEE_MODE_5) and (screen_mode != ScreenMode.SEE_MODE_6) and (screen_mode != ScreenMode.SEE_MODE_7)):
                raise LaubeException('unmatch screen_mode')

            application_number = applicationInfoDto.application_number

            if application_number is None:
                raise LaubeException('required application_number')

            re_application_number = applicationInfoDto.re_application_number
            application_form_code = applicationInfoDto.application_form_code
            if not application_form_code:
                raise LaubeException(self.E005)

            application_classification_code = applicationInfoDto.application_classification_code
            if not application_classification_code:
                raise LaubeException('required application_classification_code')

            target_company_code = applicationInfoDto.target_company_code
            if not target_company_code:
                raise LaubeException(self.E002)

            target_group_code = applicationInfoDto.target_group_code
            if not target_group_code:
                raise LaubeException(self.E003)

            target_employee_code = applicationInfoDto.target_employee_code
            if not target_employee_code:
                raise LaubeException(self.E004)

            applicant_company_code = applicationInfoDto.applicant_company_code
            if not applicant_company_code:
                raise LaubeException(self.E008)

            applicant_group_code = applicationInfoDto.applicant_group_code
            if not applicant_group_code:
                raise LaubeException(self.E009)

            applicant_employee_code = applicationInfoDto.applicant_employee_code
            if not applicant_employee_code:
                raise LaubeException(self.E010)

            apply_date = applicationInfoDto.apply_date
            if apply_date is None:
                raise LaubeException('required apply_date')

            dt = datetime.now()
            applicationObject = None

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, target_company_code, application_number)
            # 申請書ステータスが[取り下げ][否認][承認]の場合はエラー
            # if applicationObject is not None and (applicationObject.application_status == ApplicationStatus.CANCEL or applicationObject.application_status == ApplicationStatus.DENIAL or applicationObject.application_status == ApplicationStatus.APPROVED):
            if applicationObject and applicationObject.application_status in [ApplicationStatus.CANCEL, ApplicationStatus.DENIAL]:
                raise LaubeException('Application cannot be overwritten.')
            else:
                # 申請オブジェクトを設定します
                applicationObject.company_code = target_company_code
                applicationObject.application_number = application_number
                applicationObject.re_application_number = re_application_number
                applicationObject.application_form_code = application_form_code
                applicationObject.target_company_code = target_company_code
                applicationObject.target_group_code = target_group_code
                applicationObject.target_employee_code = target_employee_code
                applicationObject.applicant_company_code = applicant_company_code
                applicationObject.applicant_group_code = applicant_group_code
                applicationObject.applicant_employee_code = applicant_employee_code
                applicationObject.apply_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                applicationObject.application_status = ApplicationStatus.CANCEL  # 申請書ステータスを[取り下げ]に変更
                applicationObject.update_employee_code = applicationObject.applicant_employee_code
                # 申請書履歴オブジェクトに追加します
                self.__add_history(session, applicationObject, None, ApplicantStatus.CANCEL)

            # [未着]の承認者を全て削除します。
            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, target_company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            for activityObject in activityObjects:
                if activityObject.process_date is None:
                    activityObjectDao.delete(session, activityObject.id)

            return True

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認一覧画面のViewAPIにて呼び出される事を想定しています。

    [機能]
    承認一覧の取得を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number_list : 申請番号のリスト
        application_classification_code_list : 申請分類コードのリスト
        activity_status_list : 承認者ステータスのリスト
        function_list : 承認画面の機能リスト
        apply_date_from : 申請日_から
        apply_date_to :申請日_まで
        reaching_date_from : 到達日_から
        reaching_date_to :到達日_まで
        target_employee_code[str]: 対象者の従業員番号
        approverl_employee_code[str]: 承認者の従業員番号
        application_form_code[str]: 申請書コード
    Returns:
        count

    Raises:
        LaubeException : Laube例外
    """
    def get_activity_list_count(self, session, company_code, application_number_list, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, target_employee_code=None, approverl_employee_code=None, application_form_code=None):

        try:
            utility = Utility()

            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if not apply_date_from:
                apply_date_from = utility.convert_datetimestr_2_datetime('2007/01/17 00:00:00')

            if not apply_date_to:
                apply_date_to = utility.convert_datetimestr_2_datetime('2099/12/31 23:59:59')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            activityObjectDao = ActivityObjectDao()
            approval_list = activityObjectDao.find_activity_list(session, company_code, application_number_list, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, None, target_employee_code, approverl_employee_code, application_form_code)

            return len(approval_list)

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認一覧画面のViewAPIにて呼び出される事を想定しています。

    [機能]
    承認一覧の取得を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number_list : 申請番号のリスト
        application_classification_code_list : 申請分類コードのリスト
        activity_status_list : 承認者ステータスのリスト
        function_list : 承認画面の機能リスト
        apply_date_from : 申請日_から
        apply_date_to :申請日_まで
        reaching_date_from : 到達日_から
        reaching_date_to :到達日_まで
        承認者の従業員番号
        pagerDto: ページング
        target_employee_code[str]: 対象者の従業員番号
        approverl_employee_code[str]: 承認者の従業員番号
        application_form_code[str]: 申請書コード

    Returns:
        approverlDtoList

    Raises:
        LaubeException : Laube例外
    """
    def get_activity_list(self, session, company_code, application_number_list, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, pagerDto, target_employee_code=None, approverl_employee_code=None, application_form_code=None):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if pagerDto is None:
                pagerDto = pagerDto()
                pagerDto.pagerCount = 1
                pagerDto.limit = 20
                pass

            utility = Utility()

            if not apply_date_from:
                apply_date_from = utility.convert_datetimestr_2_datetime('2007/01/17 00:00:00')

            if not apply_date_to:
                apply_date_to = utility.convert_datetimestr_2_datetime('2099/12/31 23:59:59')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            activityObjectDao = ActivityObjectDao()
            approval_list = activityObjectDao.find_activity_list(session, company_code, application_number_list, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, pagerDto, target_employee_code, approverl_employee_code, application_form_code)

            approverlDtoList = list()

            for approval in approval_list:
                approverlDto = ApproverlDto()
                approverlDto.screen_mode = ScreenMode.SEE_MODE_1
                approverlDto.application_number = approval.ApplicationObject.application_number
                approverlDto.re_application_number = approval.ApplicationObject.re_application_number
                approverlDto.application_classification_code = approval.ApplicationClassification.application_classification_code
                approverlDto.application_classification_name = approval.ApplicationClassification.application_classification_name
                approverlDto.application_form_code = approval.ApplicationForm.application_form_code
                approverlDto.application_form_name = approval.ApplicationForm.application_form_name
                approverlDto.target_company_code = approval.ApplicationObject.target_company_code
                approverlDto.target_company_name = self.__get_company_name(session, approval.ApplicationObject.target_company_code)
                approverlDto.target_group_code = approval.ApplicationObject.target_group_code
                approverlDto.target_group_name = self.__get_group_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_group_code)
                approverlDto.target_employee_code = approval.ApplicationObject.target_employee_code
                approverlDto.target_employee_name = self.__get_employee_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_employee_code)
                approverlDto.applicant_company_code = approval.ApplicationObject.applicant_company_code
                approverlDto.applicant_company_name = self.__get_company_name(session, approval.ApplicationObject.applicant_company_code)
                approverlDto.applicant_group_code = approval.ApplicationObject.applicant_group_code
                approverlDto.applicant_group_name = self.__get_group_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_group_code)
                approverlDto.applicant_employee_code = approval.ApplicationObject.applicant_employee_code
                approverlDto.applicant_employee_name = self.__get_employee_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_employee_code)
                approverlDto.apply_date = approval.ApplicationObject.apply_date
                approverlDto.application_status = approval.ApplicationObject.application_status
                approverlDto.applicant_status = None
                approverlDto.route_type = approval.ActivityObject.route_type
                approverlDto.route_number = approval.ActivityObject.route_number
                approverlDto.approverl_company_code = approval.ActivityObject.approverl_company_code
                approverlDto.approverl_company_name = self.__get_company_name(session, approval.ActivityObject.approverl_company_code)
                approverlDto.approverl_role_code = approval.ActivityObject.approverl_role_code

                roleDao = RoleDao()
                role = roleDao.find_ix_m_role(session, approverlDto.approverl_company_code, approverlDto.approverl_role_code)

                if role is None:
                    approverlDto.approverl_role_name = None
                else:
                    approverlDto.approverl_role_name = role.role_name

                approverlDto.approverl_group_code = approval.ActivityObject.approverl_group_code
                approverlDto.approverl_group_name = self.__get_group_name(session, approval.ActivityObject.approverl_company_code, approval.ActivityObject.approverl_group_code)
                approverlDto.approverl_employee_code = approval.ActivityObject.approverl_employee_code
                approverlDto.approverl_employee_name = self.__get_employee_name(session, approval.ActivityObject.approverl_company_code, approval.ActivityObject.approverl_employee_code)
                approverlDto.deputy_approverl_company_code = approval.ActivityObject.deputy_approverl_company_code
                approverlDto.deputy_approverl_company_name = self.__get_company_name(session, approval.ActivityObject.deputy_approverl_company_code)
                approverlDto.deputy_approverl_group_code = approval.ActivityObject.deputy_approverl_group_code
                approverlDto.deputy_approverl_group_name = self.__get_group_name(session, approval.ActivityObject.deputy_approverl_company_code, approval.ActivityObject.deputy_approverl_group_code)
                approverlDto.deputy_approverl_employee_code = approval.ActivityObject.deputy_approverl_employee_code
                approverlDto.deputy_approverl_employee_name = self.__get_employee_name(session, approval.ActivityObject.deputy_approverl_company_code, approval.ActivityObject.deputy_approverl_employee_code)

                if approval.ActivityObject.deputy_contents is None:
                    approverlDto.deputy_contents = None
                else:
                    approverlDto.deputy_contents = approval.ActivityObject.deputy_contents

                approverlDto.approval_function = approval.ActivityObject.function
                approverlDto.reaching_date = approval.ActivityObject.reaching_date
                approverlDto.process_date = approval.ActivityObject.process_date
                approverlDto.activity_status = approval.ActivityObject.activity_status

                if approval.ActivityObject.approverl_comment is None:
                    approverlDto.approverl_comment = None
                else:
                    approverlDto.approverl_comment = approval.ActivityObject.approverl_comment

                # 申請書履歴オブジェクトより審査履歴を取得
                routeHistoryDao = RouteHistoryDao()
                route_history_list = routeHistoryDao.find_all_by_sort(session, approverlDto.target_company_code, approverlDto.application_number)

                for route_history in route_history_list:
                    approverlDataInfoDto = ApproverlDataInfoDto()
                    approverlDataInfoDto.company_code = route_history.company_code
                    approverlDataInfoDto.company_name = route_history.company_name
                    approverlDataInfoDto.application_number = route_history.application_number
                    approverlDataInfoDto.target_company_code = route_history.target_company_code  # 対象者の会社コード
                    approverlDataInfoDto.target_company_name = self.__get_company_name(session, route_history.target_company_code)  # 対象者の会社名
                    approverlDataInfoDto.target_group_code = route_history.target_group_code  # 対象者の部署コード
                    approverlDataInfoDto.target_group_name = self.__get_group_name(session, route_history.target_company_code, route_history.target_group_code)  # 対象者の部署名
                    approverlDataInfoDto.target_employee_code = route_history.target_company_code  # 対象者の従業員番号
                    approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, route_history.target_company_code, approval.ApplicationObject.target_employee_code)  # 対象者の従業員名
                    approverlDataInfoDto.applicant_company_code = route_history.applicant_company_code  # 申請者の会社コード
                    approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, route_history.applicant_company_code)  # 申請者の会社名
                    approverlDataInfoDto.applicant_group_code = route_history.applicant_group_code  # 申請者の部署コード
                    approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, route_history.applicant_company_code, route_history.applicant_group_code)  # 申請者の部署名
                    approverlDataInfoDto.applicant_employee_code = route_history.applicant_employee_code  # 申請者の従業員番号
                    approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, route_history.applicant_company_code, route_history.applicant_employee_code)  # 申請者の従業員名
                    approverlDataInfoDto.apply_date = route_history.apply_date  # 申請日
                    approverlDataInfoDto.application_status = route_history.application_status  # 申請書ステータス
                    approverlDataInfoDto.applicant_status = route_history.applicant_status  # 申請者ステータス
                    approverlDataInfoDto.route_type = route_history.route_type
                    approverlDataInfoDto.route_number = route_history.route_number
                    approverlDataInfoDto.approverl_company_code = route_history.approverl_company_code
                    approverlDataInfoDto.approverl_company_name = route_history.approverl_company_name
                    approverlDataInfoDto.approverl_role_code = route_history.approverl_role_code
                    approverlDataInfoDto.approverl_role_name = route_history.approverl_role_name
                    approverlDataInfoDto.approverl_group_code = route_history.approverl_group_code
                    approverlDataInfoDto.approverl_group_name = route_history.approverl_group_name
                    approverlDataInfoDto.approverl_employee_code = route_history.approverl_employee_code
                    approverlDataInfoDto.approverl_employee_name = route_history.approverl_employee_name
                    approverlDataInfoDto.deputy_approverl_company_code = route_history.deputy_approverl_company_code
                    approverlDataInfoDto.deputy_approverl_company_name = route_history.deputy_approverl_company_name
                    approverlDataInfoDto.deputy_approverl_group_code = route_history.deputy_approverl_group_code
                    approverlDataInfoDto.deputy_approverl_group_name = route_history.deputy_approverl_group_name
                    approverlDataInfoDto.deputy_approverl_employee_code = route_history.deputy_approverl_employee_code
                    approverlDataInfoDto.deputy_approverl_employee_name = route_history.deputy_approverl_employee_name
                    approverlDataInfoDto.deputy_contents = route_history.deputy_contents
                    approverlDataInfoDto.approval_function = route_history.function
                    approverlDataInfoDto.reaching_date = route_history.reaching_date
                    approverlDataInfoDto.process_date = route_history.process_date
                    approverlDataInfoDto.activity_status = route_history.activity_status
                    approverlDataInfoDto.approverl_comment = route_history.approverl_comment
                    approverlDto.approverl_data_info_list.append(approverlDataInfoDto)

                # 申請明細オブジェクトを検索します。
                activityObjectDao = ActivityObjectDao()
                activityObjects = activityObjectDao.find_by_company_code_application_number(session, approverlDto.target_company_code, approverlDto.application_number)

                for activityObject in activityObjects:

                    if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED or activityObject.activity_status == ActivityStatus.ARRIVAL or activityObject.activity_status == ActivityStatus.HOLD:

                        approverlDataInfoDto = ApproverlDataInfoDto()
                        approverlDataInfoDto.company_code = activityObject.company_code
                        approverlDataInfoDto.company_name = self.__get_company_name(session, activityObject.company_code)
                        approverlDataInfoDto.application_number = activityObject.application_number
                        approverlDataInfoDto.target_company_code = approval.ApplicationObject.target_company_code  # 対象者の会社コード
                        approverlDataInfoDto.target_company_name = self.__get_company_name(session, approval.ApplicationObject.target_company_code)  # 対象者の会社名
                        approverlDataInfoDto.target_group_code = approval.ApplicationObject.target_group_code  # 対象者の部署コード
                        approverlDataInfoDto.target_group_name = self.__get_group_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_group_code)  # 対象者の部署名
                        approverlDataInfoDto.target_employee_code = approval.ApplicationObject.target_employee_code  # 対象者の従業員番号
                        approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_employee_code)  # 対象者の従業員名
                        approverlDataInfoDto.applicant_company_code = approval.ApplicationObject.applicant_company_code  # 申請者の会社コード
                        approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, approval.ApplicationObject.applicant_company_code)  # 申請者の会社名
                        approverlDataInfoDto.applicant_group_code = approval.ApplicationObject.applicant_group_code  # 申請者の部署コード
                        approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_group_code)  # 申請者の部署名
                        approverlDataInfoDto.applicant_employee_code = approval.ApplicationObject.applicant_employee_code  # 申請者の従業員番号
                        approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_employee_code)  # 申請者の従業員名
                        approverlDataInfoDto.apply_date = approval.ApplicationObject.apply_date  # 申請日
                        approverlDataInfoDto.application_status = approval.ApplicationObject.application_status  # 申請書ステータス
                        approverlDataInfoDto.applicant_status = None  # 申請者ステータス
                        approverlDataInfoDto.route_type = activityObject.route_type
                        approverlDataInfoDto.route_number = activityObject.route_number
                        approverlDataInfoDto.approverl_company_code = activityObject.approverl_company_code
                        approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, activityObject.approverl_company_code)

                        approverlDataInfoDto.approverl_role_code = activityObject.approverl_role_code

                        roleDao = RoleDao()
                        role = roleDao.find_ix_m_role(session, activityObject.approverl_company_code, activityObject.approverl_role_code)

                        if role is None:
                            approverlDataInfoDto.approverl_role_name = None
                        else:
                            approverlDataInfoDto.approverl_role_name = role.role_name

                        approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, activityObject.approverl_company_code, activityObject.approverl_group_code)
                        approverlDataInfoDto.approverl_employee_code = activityObject.approverl_employee_code
                        approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, activityObject.approverl_company_code, activityObject.approverl_employee_code)
                        approverlDataInfoDto.deputy_approverl_company_code = activityObject.deputy_approverl_company_code
                        approverlDataInfoDto.deputy_approverl_company_name = self.__get_company_name(session, activityObject.deputy_approverl_company_code)
                        approverlDataInfoDto.deputy_approverl_group_code = activityObject.deputy_approverl_group_code
                        approverlDataInfoDto.deputy_approverl_group_name = self.__get_group_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_group_code)
                        approverlDataInfoDto.deputy_approverl_employee_code = activityObject.deputy_approverl_employee_code
                        approverlDataInfoDto.deputy_approverl_employee_name = self.__get_employee_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_employee_code)
                        approverlDataInfoDto.deputy_contents = activityObject.deputy_contents
                        approverlDataInfoDto.approval_function = activityObject.function
                        approverlDataInfoDto.reaching_date = activityObject.reaching_date
                        approverlDataInfoDto.process_date = activityObject.process_date
                        approverlDataInfoDto.activity_status = activityObject.activity_status
                        approverlDataInfoDto.approverl_comment = activityObject.approverl_comment
                        approverlDto.approverl_data_info_list.append(approverlDataInfoDto)

                approverlDtoList.append(approverlDto)

            return approverlDtoList

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    停滞一覧画面のViewAPIにて呼び出される事を想定しています。

    [機能]
    停滞一覧の取得を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        application_classification_code_list : 申請分類コードのリスト
        is_confirmation : 確認待ち
        is_approval : 承認待ち
        elapsed_date : 到着してからの経過日
        apply_date_from : 申請日_から
        apply_date_to :申請日_まで
    Returns:
        count

    Raises:
        LaubeException : Laube例外
    """
    def get_stagnation_list_count(self, session, company_code, application_number, application_classification_code_list, is_confirmation, is_approval, elapsed_date, apply_date_from, apply_date_to):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if is_confirmation is None:
                raise LaubeException('required is_confirmation')

            if is_approval is None:
                raise LaubeException('required is_approval')

            if elapsed_date is None:
                elapsed_date = 0

            utility = Utility()

            if not apply_date_from:
                apply_date_from = utility.convert_datetimestr_2_datetime('2007/01/17 00:00:00')

            if not apply_date_to:
                apply_date_to = utility.convert_datetimestr_2_datetime('2099/12/31 23:59:59')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            activityObjectDao = ActivityObjectDao()
            approval_list = activityObjectDao.find_stagnation_list(session, company_code, application_number, application_classification_code_list, is_confirmation, is_approval, elapsed_date, apply_date_from, apply_date_to, None)

            result_list = list()

            for approval in approval_list:
                is_denial_status = approval.ApplicationObject.application_status == ApplicationStatus.DENIAL
                has_activity_object = approval.ActivityObject is not None
                is_untreated_status = approval.ActivityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED
                if is_denial_status and has_activity_object and is_untreated_status:
                    continue

                result_list.append(approval)

            return len(result_list)

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    停滞一覧画面のViewAPIにて呼び出される事を想定しています。

    [機能]
    停滞一覧の取得を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        application_classification_code_list : 申請分類コードのリスト
        is_confirmation : 確認待ち
        is_approval : 承認待ち
        elapsed_date : 到着してからの経過日
        apply_date_from : 申請日_から
        apply_date_to :申請日_まで
        pagerDto: ページング

    Returns:
        approverlDtoList

    Raises:
        LaubeException : Laube例外
    """
    def get_stagnation_list(self, session, company_code, application_number, application_classification_code_list, is_confirmation, is_approval, elapsed_date, apply_date_from, apply_date_to, pagerDto):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if is_confirmation is None:
                raise LaubeException('required is_confirmation')

            if is_approval is None:
                raise LaubeException('required is_approval')

            if elapsed_date is None:
                elapsed_date = 0

            if pagerDto is None:
                pagerDto = pagerDto()
                pagerDto.pagerCount = 1
                pagerDto.limit = 20
                pass

            utility = Utility()

            if not apply_date_from:
                apply_date_from = utility.convert_datetimestr_2_datetime('2007/01/17 00:00:00')

            if not apply_date_to:
                apply_date_to = utility.convert_datetimestr_2_datetime('2099/12/31 23:59:59')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            activityObjectDao = ActivityObjectDao()
            approval_list = activityObjectDao.find_stagnation_list(session, company_code, application_number, application_classification_code_list, is_confirmation, is_approval, elapsed_date, apply_date_from, apply_date_to, pagerDto)

            result_list = list()

            for approval in approval_list:
                is_denial_status = approval.ApplicationObject.application_status == ApplicationStatus.DENIAL
                has_valid_activity_object = approval.ActivityObject is not None
                is_untreated_status = approval.ActivityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED
                if is_denial_status and has_valid_activity_object and is_untreated_status:
                    continue

                result_list.append(approval)

            approverlDtoList = list()

            for approval in result_list:
                approverlDto = ApproverlDto()
                approverlDto.screen_mode = ScreenMode.APPROVAL_MODE_4
                approverlDto.application_number = approval.ApplicationObject.application_number
                approverlDto.re_application_number = approval.ApplicationObject.re_application_number
                approverlDto.application_classification_code = approval.ApplicationClassification.application_classification_code
                approverlDto.application_classification_name = approval.ApplicationClassification.application_classification_name
                approverlDto.application_form_code = approval.ApplicationForm.application_form_code
                approverlDto.application_form_name = approval.ApplicationForm.application_form_name
                approverlDto.target_company_code = approval.ApplicationObject.target_company_code
                approverlDto.target_company_name = self.__get_company_name(session, approval.ApplicationObject.target_company_code)
                approverlDto.target_group_code = approval.ApplicationObject.target_group_code
                approverlDto.target_group_name = self.__get_group_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_group_code)
                approverlDto.target_employee_code = approval.ApplicationObject.target_employee_code
                approverlDto.target_employee_name = self.__get_employee_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_employee_code)
                approverlDto.applicant_company_code = approval.ApplicationObject.applicant_company_code
                approverlDto.applicant_company_name = self.__get_company_name(session, approval.ApplicationObject.applicant_company_code)
                approverlDto.applicant_group_code = approval.ApplicationObject.applicant_group_code
                approverlDto.applicant_group_name = self.__get_group_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_group_code)
                approverlDto.applicant_employee_code = approval.ApplicationObject.applicant_employee_code
                approverlDto.applicant_employee_name = self.__get_employee_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_employee_code)
                approverlDto.apply_date = approval.ApplicationObject.apply_date
                approverlDto.application_status = approval.ApplicationObject.application_status
                approverlDto.applicant_status = None
                approverlDto.route_type = approval.ActivityObject.route_type
                approverlDto.route_number = approval.ActivityObject.route_number
                approverlDto.approverl_company_code = approval.ActivityObject.approverl_company_code
                approverlDto.approverl_company_name = self.__get_company_name(session, approval.ActivityObject.approverl_company_code)
                approverlDto.approverl_role_code = approval.ActivityObject.approverl_role_code

                # 到着日から時刻を除去
                reaching_date = utility.convert_datetime_2_date(approval.ActivityObject.reaching_date)

                dt = datetime.now()
                system_date = utility.convert_datetime_2_date(dt)
                # 経過日数
                approverlDto.stagnation_days = (system_date - reaching_date).days

                roleDao = RoleDao()
                role = roleDao.find_ix_m_role(session, approverlDto.approverl_company_code, approverlDto.approverl_role_code)

                if role is None:
                    approverlDto.approverl_role_name = None
                else:
                    approverlDto.approverl_role_name = role.role_name

                approverlDto.approverl_group_code = approval.ActivityObject.approverl_group_code
                approverlDto.approverl_group_name = self.__get_group_name(session, approval.ActivityObject.approverl_company_code, approval.ActivityObject.approverl_group_code)
                approverlDto.approverl_employee_code = approval.ActivityObject.approverl_employee_code
                approverlDto.approverl_employee_name = self.__get_employee_name(session, approval.ActivityObject.approverl_company_code, approval.ActivityObject.approverl_employee_code)
                approverlDto.deputy_approverl_company_code = approval.ActivityObject.deputy_approverl_company_code
                approverlDto.deputy_approverl_company_name = self.__get_company_name(session, approval.ActivityObject.deputy_approverl_company_code)
                approverlDto.deputy_approverl_group_code = approval.ActivityObject.deputy_approverl_group_code
                approverlDto.deputy_approverl_group_name = self.__get_group_name(session, approval.ActivityObject.deputy_approverl_company_code, approval.ActivityObject.deputy_approverl_group_code)
                approverlDto.deputy_approverl_employee_code = approval.ActivityObject.deputy_approverl_employee_code
                approverlDto.deputy_approverl_employee_name = self.__get_employee_name(session, approval.ActivityObject.deputy_approverl_company_code, approval.ActivityObject.deputy_approverl_employee_code)
                approverlDto.deputy_contents = approval.ActivityObject.deputy_contents
                approverlDto.approval_function = approval.ActivityObject.function
                approverlDto.reaching_date = approval.ActivityObject.reaching_date
                approverlDto.process_date = approval.ActivityObject.process_date
                approverlDto.activity_status = approval.ActivityObject.activity_status
                approverlDto.approverl_comment = approval.ActivityObject.approverl_comment

                # 申請書履歴オブジェクトより審査履歴を取得
                routeHistoryDao = RouteHistoryDao()
                route_history_list = routeHistoryDao.find_all_by_sort(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.application_number)

                for route_history in route_history_list:
                    approverlDataInfoDto = ApproverlDataInfoDto()
                    approverlDataInfoDto.company_code = route_history.company_code
                    approverlDataInfoDto.company_name = route_history.company_name
                    approverlDataInfoDto.application_number = route_history.application_number
                    approverlDataInfoDto.target_company_code = route_history.target_company_code  # 対象者の会社コード
                    approverlDataInfoDto.target_company_name = self.__get_company_name(session, route_history.target_company_code)  # 対象者の会社名
                    approverlDataInfoDto.target_group_code = route_history.target_group_code  # 対象者の部署コード
                    approverlDataInfoDto.target_group_name = self.__get_group_name(session, route_history.target_company_code, route_history.target_group_code)  # 対象者の部署名
                    approverlDataInfoDto.target_employee_code = route_history.target_employee_code  # 対象者の従業員番号
                    approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, route_history.target_company_code, route_history.target_employee_code)  # 対象者の従業員名
                    approverlDataInfoDto.applicant_company_code = route_history.applicant_company_code  # 申請者の会社コード
                    approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, route_history.applicant_company_code)  # 申請者の会社名
                    approverlDataInfoDto.applicant_group_code = route_history.applicant_group_code  # 申請者の部署コード
                    approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, route_history.applicant_company_code, route_history.applicant_group_code)  # 申請者の部署名
                    approverlDataInfoDto.applicant_employee_code = route_history.applicant_employee_code  # 申請者の従業員番号
                    approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, route_history.applicant_company_code, route_history.applicant_employee_code)  # 申請者の従業員名
                    approverlDataInfoDto.apply_date = route_history.apply_date  # 申請日
                    approverlDataInfoDto.application_status = route_history.application_status  # 申請書ステータス
                    approverlDataInfoDto.applicant_status = route_history.applicant_status  # 申請者ステータス
                    approverlDataInfoDto.route_type = route_history.route_type
                    approverlDataInfoDto.route_number = route_history.route_number
                    approverlDataInfoDto.approverl_company_code = route_history.approverl_company_code
                    approverlDataInfoDto.approverl_company_name = route_history.approverl_company_name
                    approverlDataInfoDto.approverl_role_code = route_history.approverl_role_code
                    approverlDataInfoDto.approverl_role_name = route_history.approverl_role_name
                    approverlDataInfoDto.approverl_group_code = route_history.approverl_group_code
                    approverlDataInfoDto.approverl_group_name = route_history.approverl_group_name
                    approverlDataInfoDto.approverl_employee_code = route_history.approverl_employee_code
                    approverlDataInfoDto.approverl_employee_name = route_history.approverl_employee_name
                    approverlDataInfoDto.deputy_approverl_company_code = route_history.deputy_approverl_company_code
                    approverlDataInfoDto.deputy_approverl_company_name = route_history.deputy_approverl_company_name
                    approverlDataInfoDto.deputy_approverl_group_code = route_history.deputy_approverl_group_code
                    approverlDataInfoDto.deputy_approverl_group_name = route_history.deputy_approverl_group_name
                    approverlDataInfoDto.deputy_approverl_employee_code = route_history.deputy_approverl_employee_code
                    approverlDataInfoDto.deputy_approverl_employee_name = route_history.deputy_approverl_employee_name
                    approverlDataInfoDto.deputy_contents = route_history.deputy_contents
                    approverlDataInfoDto.approval_function = route_history.function
                    approverlDataInfoDto.reaching_date = route_history.reaching_date
                    approverlDataInfoDto.process_date = route_history.process_date
                    approverlDataInfoDto.activity_status = route_history.activity_status
                    approverlDataInfoDto.approverl_comment = route_history.approverl_comment
                    approverlDto.approverl_data_info_list.append(approverlDataInfoDto)

                # 申請明細オブジェクトを検索します。
                activityObjectDao = ActivityObjectDao()
                activityObjects = activityObjectDao.find_by_company_code_application_number(session, approverlDto.target_company_code, approverlDto.application_number)

                for activityObject in activityObjects:

                    if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED or activityObject.activity_status == ActivityStatus.ARRIVAL or activityObject.activity_status == ActivityStatus.HOLD:

                        approverlDataInfoDto = ApproverlDataInfoDto()
                        approverlDataInfoDto.company_code = activityObject.company_code
                        approverlDataInfoDto.company_name = self.__get_company_name(session, activityObject.company_code)
                        approverlDataInfoDto.application_number = activityObject.application_number
                        approverlDataInfoDto.target_company_code = approval.ApplicationObject.target_company_code  # 対象者の会社コード
                        approverlDataInfoDto.target_company_name = self.__get_company_name(session, approval.ApplicationObject.target_company_code)  # 対象者の会社名
                        approverlDataInfoDto.target_group_code = approval.ApplicationObject.target_group_code  # 対象者の部署コード
                        approverlDataInfoDto.target_group_name = self.__get_group_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_group_code)  # 対象者の部署名
                        approverlDataInfoDto.target_employee_code = approval.ApplicationObject.target_employee_code  # 対象者の従業員番号
                        approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_employee_code)  # 対象者の従業員名
                        approverlDataInfoDto.applicant_company_code = approval.ApplicationObject.applicant_company_code  # 申請者の会社コード
                        approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, approval.ApplicationObject.applicant_company_code)  # 申請者の会社名
                        approverlDataInfoDto.applicant_group_code = approval.ApplicationObject.applicant_group_code  # 申請者の部署コード
                        approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_group_code)  # 申請者の部署名
                        approverlDataInfoDto.applicant_employee_code = approval.ApplicationObject.applicant_employee_code  # 申請者の従業員番号
                        approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_employee_code)  # 申請者の従業員名
                        approverlDataInfoDto.apply_date = approval.ApplicationObject.apply_date  # 申請日
                        approverlDataInfoDto.application_status = approval.ApplicationObject.application_status  # 申請書ステータス
                        approverlDataInfoDto.applicant_status = None  # 申請者ステータス
                        approverlDataInfoDto.route_type = activityObject.route_type
                        approverlDataInfoDto.route_number = activityObject.route_number
                        approverlDataInfoDto.approverl_company_code = activityObject.approverl_company_code
                        approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, activityObject.approverl_company_code)
                        approverlDataInfoDto.approverl_role_code = activityObject.approverl_role_code

                        roleDao = RoleDao()
                        role = roleDao.find_ix_m_role(session, activityObject.approverl_company_code, activityObject.approverl_role_code)

                        if role is None:
                            approverlDataInfoDto.approverl_role_name = None
                        else:
                            approverlDataInfoDto.approverl_role_name = role.role_name

                        approverlDataInfoDto.approverl_group_code = activityObject.approverl_group_code
                        approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, activityObject.approverl_company_code, activityObject.approverl_group_code)
                        approverlDataInfoDto.approverl_employee_code = activityObject.approverl_employee_code
                        approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, activityObject.approverl_company_code, activityObject.approverl_employee_code)
                        approverlDataInfoDto.deputy_approverl_company_code = activityObject.deputy_approverl_company_code
                        approverlDataInfoDto.deputy_approverl_company_name = self.__get_company_name(session, activityObject.deputy_approverl_company_code)
                        approverlDataInfoDto.deputy_approverl_group_code = activityObject.deputy_approverl_group_code
                        approverlDataInfoDto.deputy_approverl_group_name = self.__get_group_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_group_code)
                        approverlDataInfoDto.deputy_approverl_employee_code = activityObject.deputy_approverl_employee_code
                        approverlDataInfoDto.deputy_approverl_employee_name = self.__get_employee_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_employee_code)
                        approverlDataInfoDto.deputy_contents = activityObject.deputy_contents
                        approverlDataInfoDto.approval_function = activityObject.function
                        approverlDataInfoDto.reaching_date = activityObject.reaching_date
                        approverlDataInfoDto.process_date = activityObject.process_date
                        approverlDataInfoDto.activity_status = activityObject.activity_status
                        approverlDataInfoDto.approverl_comment = activityObject.approverl_comment
                        approverlDto.approverl_data_info_list.append(approverlDataInfoDto)

                approverlDtoList.append(approverlDto)

            return approverlDtoList

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認状況画面のViewAPIにて呼び出される事を想定しています。

    [機能]
    承認状況の取得を行います。

    Args:
        session : セッション情報
        application_number_list : 申請番号のリスト
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        application_classification_code_list:申請分類リスト
        activity_status_list:承認者ステータスリスト
        function_list:承認画面の機能リスト
        apply_date_from:申請日[開始]
        apply_date_to:申請日[終了]
        reaching_date_from : 到達日_から
        reaching_date_to :到達日_まで
    Returns:
        count

    Raises:
        LaubeException : Laube例外
    """
    def get_approval_target_list_count(self, session, application_number_list, approverl_company_code, approverl_group_code, approverl_employee_code, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, application_form_code=None):

        try:
            if not session:
                raise LaubeException(self.E001)

            approval_list = list()
            approverl_role_code_list = list()

            if approverl_group_code is not None:
                employeeGroupRoleDao = EmployeeGroupRoleDao()
                employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
                if employeeGroupRoles is None:
                    pass
                else:
                    for employeeGroupRole in employeeGroupRoles:
                        approverl_role_code_list.append(employeeGroupRole.role_code)

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, approverl_company_code)

            activityObjectDao = ActivityObjectDao()
            approval_list = activityObjectDao.find_approval_target_list(session, application_number_list, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, None, application_form_code)

            if approval_list is None:
                approval_list = list()

            deputy_approvel_list = None

            if approverl_group_code is not None:
                # 代理承認者マスタを参照
                deputyApprovelDao = DeputyApprovelDao()
                deputy_approvel_list = deputyApprovelDao.find_all_deputy_approvel(session, approverl_company_code, approverl_group_code, approverl_employee_code)

            if deputy_approvel_list is None:
                pass
            else:
                for deputy_approvel in deputy_approvel_list:
                    _list = activityObjectDao.find_approval_target_list(session, application_number_list, deputy_approvel.company_code, deputy_approvel.group_code, deputy_approvel.employee_code, approverl_role_code_list, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, None, application_form_code)
                    if _list is None:
                        _list = list()

                    for record in _list:
                        approval_list.append(record)

            result_list = list()

            for approval in approval_list:
                if approval.ApplicationObject.application_status == ApplicationStatus.DENIAL and approval.ActivityObject is not None and approval.ActivityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED:
                    continue

                result_list.append(approval)

            return len(result_list)

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認状況画面のViewAPIにて呼び出される事を想定しています。

    [機能]
    承認状況の取得を行います。

    Args:
        session : セッション情報
        application_number : 申請番号
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        application_classification_code_list:申請分類リスト
        activity_status_list:承認者ステータスリスト
        function_list:承認画面の機能リスト
        apply_date_from:申請日[開始]
        apply_date_to:申請日[終了]
        reaching_date_from : 到達日_から
        reaching_date_to :到達日_まで
        pagerDto: ページング
    Returns:
        approverlDtoList

    Raises:
        LaubeException : Laube例外
    """
    def get_approval_target_list(self, session, application_number_list, approverl_company_code, approverl_group_code, approverl_employee_code, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, pagerDto, application_form_code=None):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            if pagerDto is None:
                pagerDto = pagerDto()
                pagerDto.pagerCount = 1
                pagerDto.limit = 20
                pass

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, approverl_company_code)

            approverl_role_code_list = list()

            if approverl_group_code is not None:
                employeeGroupRoleDao = EmployeeGroupRoleDao()
                employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
                if employeeGroupRoles is None:
                    pass
                else:
                    for employeeGroupRole in employeeGroupRoles:
                        approverl_role_code_list.append(employeeGroupRole.role_code)

            activityObjectDao = ActivityObjectDao()
            approval_list = activityObjectDao.find_approval_target_list(session, application_number_list, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, pagerDto, application_form_code)

            if approval_list is None:
                approval_list = list()

            deputy_approvel_list = None

            if approverl_group_code is not None:
                # 代理承認者マスタを参照
                deputyApprovelDao = DeputyApprovelDao()
                deputy_approvel_list = deputyApprovelDao.find_all_deputy_approvel(session, approverl_company_code, approverl_group_code, approverl_employee_code)

            if deputy_approvel_list is None:
                pass
            else:
                for deputy_approvel in deputy_approvel_list:
                    _list = activityObjectDao.find_approval_target_list(session, application_number_list, deputy_approvel.company_code, deputy_approvel.group_code, deputy_approvel.employee_code, approverl_role_code_list, application_classification_code_list, activity_status_list, function_list, apply_date_from, apply_date_to, reaching_date_from, reaching_date_to, pagerDto, application_form_code)
                    if _list is None:
                        _list = list()

                    for record in _list:
                        approval_list.append(record)

            result_list = list()
            approverlDtoList = list()

            for approval in approval_list:
                if approval.ApplicationObject.application_status == ApplicationStatus.DENIAL and approval.ActivityObject is not None and approval.ActivityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED:
                    continue

                result_list.append(approval)

            for approval in result_list:

                approverlDto = ApproverlDto()

                if ApprovalFunction.EXAMINATION == approval.ActivityObject.function:  # 審査

                    if ActivityStatus.AUTHORIZER_UNTREATED == approval.ActivityObject.activity_status:  # 未処理
                        if ApplicationStatus.UNDER_EXAMINATION == approval.ApplicationObject.application_status:  # 審査中の場合
                            approverlDto.screen_mode = ScreenMode.APPROVAL_MODE_3  # 承認モード3[先取り/引き上げ]
                        else:
                            approverlDto.screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1[ボタンなし]

                    elif ActivityStatus.ARRIVAL == approval.ActivityObject.activity_status:  # 到着
                        approverlDto.screen_mode = ScreenMode.APPROVAL_MODE_1  # 承認モード1[承認/否認/差戻し/保留]

                    elif ActivityStatus.HOLD == approval.ActivityObject.activity_status:  # 保留
                        approverlDto.screen_mode = ScreenMode.APPROVAL_MODE_1  # 承認モード1[承認/否認/差戻し/保留]

                    else:
                        approverlDto.screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1[ボタンなし]

                elif ApprovalFunction.FUNCTION_CONFIRMATION == approval.ActivityObject.function:  # 確認

                    if ActivityStatus.ARRIVAL == approval.ActivityObject.activity_status:  # 到着
                        approverlDto.screen_mode = ScreenMode.CONFIRMATION_MODE  # 確認モード [確認]

                    else:
                        approverlDto.screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1[ボタンなし]

                elif ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL == approval.ActivityObject.function:  # 自動承認
                    approverlDto.screen_mode = ScreenMode.SEE_MODE_1  # 参照モード1[ボタンなし]

                approverlDto.application_number = approval.ApplicationObject.application_number
                approverlDto.re_application_number = approval.ApplicationObject.re_application_number
                approverlDto.application_classification_code = approval.ApplicationClassification.application_classification_code
                approverlDto.application_classification_name = approval.ApplicationClassification.application_classification_name
                approverlDto.application_form_code = approval.ApplicationForm.application_form_code
                approverlDto.application_form_name = approval.ApplicationForm.application_form_name
                approverlDto.target_company_code = approval.ApplicationObject.target_company_code
                approverlDto.target_company_name = self.__get_company_name(session, approval.ApplicationObject.target_company_code)
                approverlDto.target_group_code = approval.ApplicationObject.target_group_code
                approverlDto.target_group_name = self.__get_group_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_group_code)
                approverlDto.target_employee_code = approval.ApplicationObject.target_employee_code
                approverlDto.target_employee_name = self.__get_employee_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_employee_code)
                approverlDto.applicant_company_code = approval.ApplicationObject.applicant_company_code
                approverlDto.applicant_company_name = self.__get_company_name(session, approval.ApplicationObject.applicant_company_code)
                approverlDto.applicant_group_code = approval.ApplicationObject.applicant_group_code
                approverlDto.applicant_group_name = self.__get_group_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_group_code)
                approverlDto.applicant_employee_code = approval.ApplicationObject.applicant_employee_code
                approverlDto.applicant_employee_name = self.__get_employee_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_employee_code)
                approverlDto.apply_date = approval.ApplicationObject.apply_date
                approverlDto.application_status = approval.ApplicationObject.application_status
                approverlDto.applicant_status = None
                approverlDto.route_type = approval.ActivityObject.route_type
                approverlDto.route_number = approval.ActivityObject.route_number
                approverlDto.approverl_company_code = approval.ActivityObject.approverl_company_code
                approverlDto.approverl_company_name = self.__get_company_name(session, approval.ActivityObject.approverl_company_code)
                approverlDto.approverl_role_code = approval.ActivityObject.approverl_role_code

                roleDao = RoleDao()
                role = roleDao.find_ix_m_role(session, approverlDto.approverl_company_code, approverlDto.approverl_role_code)

                if role is None:
                    approverlDto.approverl_role_name = None
                else:
                    approverlDto.approverl_role_name = role.role_name

                approverlDto.approverl_group_code = approval.ActivityObject.approverl_group_code
                approverlDto.approverl_group_name = self.__get_group_name(session, approval.ActivityObject.approverl_company_code, approval.ActivityObject.approverl_group_code)
                approverlDto.approverl_employee_code = approval.ActivityObject.approverl_employee_code
                approverlDto.approverl_employee_name = self.__get_employee_name(session, approval.ActivityObject.approverl_company_code, approval.ActivityObject.approverl_employee_code)
                approverlDto.deputy_approverl_company_code = approval.ActivityObject.deputy_approverl_company_code
                approverlDto.deputy_approverl_company_name = self.__get_company_name(session, approval.ActivityObject.deputy_approverl_company_code)
                approverlDto.deputy_approverl_group_code = approval.ActivityObject.deputy_approverl_group_code
                approverlDto.deputy_approverl_group_name = self.__get_group_name(session, approval.ActivityObject.deputy_approverl_company_code, approval.ActivityObject.deputy_approverl_group_code)
                approverlDto.deputy_approverl_employee_code = approval.ActivityObject.deputy_approverl_employee_code
                approverlDto.deputy_approverl_employee_name = self.__get_employee_name(session, approval.ActivityObject.deputy_approverl_company_code, approval.ActivityObject.deputy_approverl_employee_code)
                approverlDto.deputy_contents = approval.ActivityObject.deputy_contents
                approverlDto.approval_function = approval.ActivityObject.function
                approverlDto.reaching_date = approval.ActivityObject.reaching_date
                approverlDto.process_date = approval.ActivityObject.process_date
                approverlDto.activity_status = approval.ActivityObject.activity_status
                approverlDto.approverl_comment = approval.ActivityObject.approverl_comment

                # 申請書履歴オブジェクトより審査履歴を取得
                routeHistoryDao = RouteHistoryDao()
                route_history_list = routeHistoryDao.find_all_by_sort(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.application_number)

                for route_history in route_history_list:
                    approverlDataInfoDto = ApproverlDataInfoDto()
                    approverlDataInfoDto.company_code = route_history.company_code
                    approverlDataInfoDto.company_name = route_history.company_name
                    approverlDataInfoDto.application_number = route_history.application_number
                    approverlDataInfoDto.target_company_code = route_history.target_company_code  # 対象者の会社コード
                    approverlDataInfoDto.target_company_name = self.__get_company_name(session, route_history.target_company_code)  # 対象者の会社名
                    approverlDataInfoDto.target_group_code = route_history.target_group_code  # 対象者の部署コード
                    approverlDataInfoDto.target_group_name = self.__get_group_name(session, route_history.target_company_code, route_history.target_group_code)  # 対象者の部署名
                    approverlDataInfoDto.target_employee_code = route_history.target_employee_code  # 対象者の従業員番号
                    approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, route_history.target_company_code, route_history.target_employee_code)  # 対象者の従業員名
                    approverlDataInfoDto.applicant_company_code = route_history.applicant_company_code  # 申請者の会社コード
                    approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, route_history.applicant_company_code)  # 申請者の会社名
                    approverlDataInfoDto.applicant_group_code = route_history.applicant_group_code  # 申請者の部署コード
                    approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, route_history.applicant_company_code, route_history.applicant_group_code)  # 申請者の部署名
                    approverlDataInfoDto.applicant_employee_code = route_history.applicant_employee_code  # 申請者の従業員番号
                    approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, route_history.applicant_company_code, route_history.applicant_employee_code)  # 申請者の従業員名
                    approverlDataInfoDto.apply_date = route_history.apply_date  # 申請日
                    approverlDataInfoDto.application_status = route_history.application_status  # 申請書ステータス
                    approverlDataInfoDto.applicant_status = route_history.applicant_status  # 申請者ステータス
                    approverlDataInfoDto.route_type = route_history.route_type
                    approverlDataInfoDto.route_number = route_history.route_number
                    approverlDataInfoDto.approverl_company_code = route_history.approverl_company_code
                    approverlDataInfoDto.approverl_company_name = route_history.approverl_company_name
                    approverlDataInfoDto.approverl_role_code = route_history.approverl_role_code
                    approverlDataInfoDto.approverl_role_name = route_history.approverl_role_name
                    approverlDataInfoDto.approverl_group_code = route_history.approverl_group_code
                    approverlDataInfoDto.approverl_group_name = route_history.approverl_group_name
                    approverlDataInfoDto.approverl_employee_code = route_history.approverl_employee_code
                    approverlDataInfoDto.approverl_employee_name = route_history.approverl_employee_name
                    approverlDataInfoDto.deputy_approverl_company_code = route_history.deputy_approverl_company_code
                    approverlDataInfoDto.deputy_approverl_company_name = route_history.deputy_approverl_company_name
                    approverlDataInfoDto.deputy_approverl_group_code = route_history.deputy_approverl_group_code
                    approverlDataInfoDto.deputy_approverl_group_name = route_history.deputy_approverl_group_name
                    approverlDataInfoDto.deputy_approverl_employee_code = route_history.deputy_approverl_employee_code
                    approverlDataInfoDto.deputy_approverl_employee_name = route_history.deputy_approverl_employee_name
                    approverlDataInfoDto.deputy_contents = route_history.deputy_contents
                    approverlDataInfoDto.approval_function = route_history.function
                    approverlDataInfoDto.reaching_date = route_history.reaching_date
                    approverlDataInfoDto.process_date = route_history.process_date
                    approverlDataInfoDto.activity_status = route_history.activity_status
                    approverlDataInfoDto.approverl_comment = route_history.approverl_comment
                    approverlDto.approverl_data_info_list.append(approverlDataInfoDto)

                # 申請明細オブジェクトを検索します。
                activityObjectDao = ActivityObjectDao()
                activityObjects = activityObjectDao.find_by_company_code_application_number(session, approverlDto.target_company_code, approverlDto.application_number)

                for activityObject in activityObjects:

                    if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED or activityObject.activity_status == ActivityStatus.ARRIVAL or activityObject.activity_status == ActivityStatus.HOLD:

                        approverlDataInfoDto = ApproverlDataInfoDto()
                        approverlDataInfoDto.company_code = activityObject.company_code
                        approverlDataInfoDto.company_name = self.__get_company_name(session, activityObject.company_code)
                        approverlDataInfoDto.application_number = activityObject.application_number
                        approverlDataInfoDto.target_company_code = approval.ApplicationObject.target_company_code  # 対象者の会社コード
                        approverlDataInfoDto.target_company_name = self.__get_company_name(session, approval.ApplicationObject.target_company_code)  # 対象者の会社名
                        approverlDataInfoDto.target_group_code = approval.ApplicationObject.target_group_code  # 対象者の部署コード
                        approverlDataInfoDto.target_group_name = self.__get_group_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_group_code)  # 対象者の部署名
                        approverlDataInfoDto.target_employee_code = approval.ApplicationObject.target_employee_code  # 対象者の従業員番号
                        approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_employee_code)  # 対象者の従業員名
                        approverlDataInfoDto.applicant_company_code = approval.ApplicationObject.applicant_company_code  # 申請者の会社コード
                        approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, approval.ApplicationObject.applicant_company_code)  # 申請者の会社名
                        approverlDataInfoDto.applicant_group_code = approval.ApplicationObject.applicant_group_code  # 申請者の部署コード
                        approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_group_code)  # 申請者の部署名
                        approverlDataInfoDto.applicant_employee_code = approval.ApplicationObject.applicant_employee_code  # 申請者の従業員番号
                        approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_employee_code)  # 申請者の従業員名
                        approverlDataInfoDto.apply_date = approval.ApplicationObject.apply_date  # 申請日
                        approverlDataInfoDto.application_status = approval.ApplicationObject.application_status  # 申請書ステータス
                        approverlDataInfoDto.applicant_status = None  # 申請者ステータス
                        approverlDataInfoDto.route_type = activityObject.route_type
                        approverlDataInfoDto.route_number = activityObject.route_number
                        approverlDataInfoDto.approverl_company_code = activityObject.approverl_company_code
                        approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, activityObject.approverl_company_code)
                        approverlDataInfoDto.approverl_role_code = activityObject.approverl_role_code

                        roleDao = RoleDao()
                        role = roleDao.find_ix_m_role(session, activityObject.approverl_company_code, activityObject.approverl_role_code)

                        if role is None:
                            approverlDataInfoDto.approverl_role_name = None
                        else:
                            approverlDataInfoDto.approverl_role_name = role.role_name

                        approverlDataInfoDto.approverl_group_code = activityObject.approverl_group_code
                        approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, activityObject.approverl_company_code, activityObject.approverl_group_code)
                        approverlDataInfoDto.approverl_employee_code = activityObject.approverl_employee_code
                        approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, activityObject.approverl_company_code, activityObject.approverl_employee_code)
                        approverlDataInfoDto.deputy_approverl_company_code = activityObject.deputy_approverl_company_code
                        approverlDataInfoDto.deputy_approverl_company_name = self.__get_company_name(session, activityObject.deputy_approverl_company_code)
                        approverlDataInfoDto.deputy_approverl_group_code = activityObject.deputy_approverl_group_code
                        approverlDataInfoDto.deputy_approverl_group_name = self.__get_group_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_group_code)
                        approverlDataInfoDto.deputy_approverl_employee_code = activityObject.deputy_approverl_employee_code
                        approverlDataInfoDto.deputy_approverl_employee_name = self.__get_employee_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_employee_code)
                        approverlDataInfoDto.deputy_contents = activityObject.deputy_contents
                        approverlDataInfoDto.approval_function = activityObject.function
                        approverlDataInfoDto.reaching_date = activityObject.reaching_date
                        approverlDataInfoDto.process_date = activityObject.process_date
                        approverlDataInfoDto.activity_status = activityObject.activity_status
                        approverlDataInfoDto.approverl_comment = activityObject.approverl_comment
                        approverlDto.approverl_data_info_list.append(approverlDataInfoDto)

                approverlDtoList.append(approverlDto)
            if approverlDtoList is not None and len(approverlDtoList) > 0:
                approverlDtoList = sorted(approverlDtoList, key=lambda x: (x.application_number), reverse=True)
            return approverlDtoList

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    下記のInitAPIにて呼び出される事を想定しています。
    承認一覧画面[詳細]のInitAPI
    承認状況画面[詳細]のInitAPI
    停滞一覧画面[詳細]のInitAPI

    [機能]
    承認情報を返却します。

    Args:
        session : セッション情報
        screen_mode: 画面モード
        company_code : 会社コード
        application_number : 申請番号
        route_type : ルートタイプ
        route_number : ルート番号
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        role_code : ロールコード

    Returns:
        選択された申請書

    Raises:
        Exception : 例外
    """
    def find_approval(self, session, screen_mode, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, role_code=None):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if application_number is None:
                raise LaubeException('required application_number')

            if route_type is None:
                raise LaubeException('required route_type')

            if route_number is None:
                raise LaubeException('required route_number')

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            approverl_role_code_list = list()
            if approverl_company_code is not None and approverl_group_code is not None and approverl_employee_code is not None:
                employeeGroupRoleDao = EmployeeGroupRoleDao()
                employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
                if employeeGroupRoles is None:
                    pass
                else:
                    for employeeGroupRole in employeeGroupRoles:
                        approverl_role_code_list.append(employeeGroupRole.role_code)

            activityObjectDao = ActivityObjectDao()
            approval = activityObjectDao.find_activity_object(session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list, role_code)

            if approval is None:
                raise LaubeException('missing approval')

            approverlDto = ApproverlDto()
            approverlDto.application_number = approval.ApplicationObject.application_number
            approverlDto.re_application_number = approval.ApplicationObject.re_application_number
            approverlDto.application_classification_code = approval.ApplicationClassification.application_classification_code
            approverlDto.application_classification_name = approval.ApplicationClassification.application_classification_name
            approverlDto.application_form_code = approval.ApplicationForm.application_form_code
            approverlDto.application_form_name = approval.ApplicationForm.application_form_name
            approverlDto.target_company_code = approval.ApplicationObject.target_company_code
            approverlDto.target_company_name = self.__get_company_name(session, approval.ApplicationObject.target_company_code)
            approverlDto.target_group_code = approval.ApplicationObject.target_group_code
            approverlDto.target_group_name = self.__get_group_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_group_code)
            approverlDto.target_employee_code = approval.ApplicationObject.target_employee_code
            approverlDto.target_employee_name = self.__get_employee_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_employee_code)
            approverlDto.applicant_company_code = approval.ApplicationObject.applicant_company_code
            approverlDto.applicant_company_name = self.__get_company_name(session, approval.ApplicationObject.applicant_company_code)
            approverlDto.applicant_group_code = approval.ApplicationObject.applicant_group_code
            approverlDto.applicant_group_name = self.__get_group_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_group_code)
            approverlDto.applicant_employee_code = approval.ApplicationObject.applicant_employee_code
            approverlDto.applicant_employee_name = self.__get_employee_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_employee_code)
            approverlDto.apply_date = approval.ApplicationObject.apply_date
            approverlDto.application_status = approval.ApplicationObject.application_status
            approverlDto.applicant_status = None
            approverlDto.route_type = approval.ActivityObject.route_type
            approverlDto.route_number = approval.ActivityObject.route_number
            approverlDto.approverl_company_code = approval.ActivityObject.approverl_company_code
            approverlDto.approverl_company_name = self.__get_company_name(session, approval.ActivityObject.approverl_company_code)
            approverlDto.approverl_role_code = approval.ActivityObject.approverl_role_code

            roleDao = RoleDao()
            role = roleDao.find_ix_m_role(session, approverlDto.approverl_company_code, approverlDto.approverl_role_code)

            if role is None:
                approverlDto.approverl_role_name = None
            else:
                approverlDto.approverl_role_name = role.role_name

            approverlDto.approverl_group_code = approval.ActivityObject.approverl_group_code
            approverlDto.approverl_group_name = self.__get_group_name(session, approval.ActivityObject.approverl_company_code, approval.ActivityObject.approverl_group_code)
            approverlDto.approverl_employee_code = approval.ActivityObject.approverl_employee_code
            approverlDto.approverl_employee_name = self.__get_employee_name(session, approval.ActivityObject.approverl_company_code, approval.ActivityObject.approverl_employee_code)
            approverlDto.deputy_approverl_company_code = approval.ActivityObject.deputy_approverl_company_code
            approverlDto.deputy_approverl_company_name = self.__get_company_name(session, approval.ActivityObject.deputy_approverl_company_code)
            approverlDto.deputy_approverl_group_code = approval.ActivityObject.deputy_approverl_group_code
            approverlDto.deputy_approverl_group_name = self.__get_group_name(session, approval.ActivityObject.deputy_approverl_company_code, approval.ActivityObject.deputy_approverl_group_code)
            approverlDto.deputy_approverl_employee_code = approval.ActivityObject.deputy_approverl_employee_code
            approverlDto.deputy_approverl_employee_name = self.__get_employee_name(session, approval.ActivityObject.deputy_approverl_company_code, approval.ActivityObject.deputy_approverl_employee_code)
            approverlDto.deputy_contents = approval.ActivityObject.deputy_contents
            approverlDto.approval_function = approval.ActivityObject.function
            approverlDto.reaching_date = approval.ActivityObject.reaching_date
            approverlDto.process_date = approval.ActivityObject.process_date
            approverlDto.activity_status = approval.ActivityObject.activity_status
            approverlDto.approverl_comment = approval.ActivityObject.approverl_comment
            approverlDto.screen_mode = screen_mode

            # 申請書履歴オブジェクトより審査履歴を取得
            routeHistoryDao = RouteHistoryDao()
            route_history_list = routeHistoryDao.find_all_by_sort(session, approverlDto.target_company_code, approverlDto.application_number)

            for route_history in route_history_list:
                approverlDataInfoDto = ApproverlDataInfoDto()
                approverlDataInfoDto.company_code = route_history.company_code
                approverlDataInfoDto.company_name = route_history.company_name
                approverlDataInfoDto.application_number = route_history.application_number
                approverlDataInfoDto.target_company_code = route_history.target_company_code  # 対象者の会社コード
                approverlDataInfoDto.target_company_name = self.__get_company_name(session, route_history.target_company_code)  # 対象者の会社名
                approverlDataInfoDto.target_group_code = route_history.target_group_code  # 対象者の部署コード
                approverlDataInfoDto.target_group_name = self.__get_group_name(session, route_history.target_company_code, route_history.target_group_code)  # 対象者の部署名
                approverlDataInfoDto.target_employee_code = route_history.target_employee_code  # 対象者の従業員番号
                approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, route_history.target_company_code, route_history.target_employee_code)  # 対象者の従業員名
                approverlDataInfoDto.applicant_company_code = route_history.applicant_company_code  # 申請者の会社コード
                approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, route_history.applicant_company_code)  # 申請者の会社名
                approverlDataInfoDto.applicant_group_code = route_history.applicant_group_code  # 申請者の部署コード
                approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, route_history.applicant_company_code, route_history.applicant_group_code)  # 申請者の部署名
                approverlDataInfoDto.applicant_employee_code = route_history.applicant_employee_code  # 申請者の従業員番号
                approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, route_history.applicant_company_code, route_history.applicant_employee_code)  # 申請者の従業員名
                approverlDataInfoDto.apply_date = route_history.apply_date  # 申請日
                approverlDataInfoDto.application_status = route_history.application_status  # 申請書ステータス
                approverlDataInfoDto.applicant_status = route_history.applicant_status  # 申請者ステータス
                approverlDataInfoDto.route_type = route_history.route_type
                approverlDataInfoDto.route_number = route_history.route_number
                approverlDataInfoDto.approverl_company_code = route_history.approverl_company_code
                approverlDataInfoDto.approverl_company_name = route_history.approverl_company_name
                approverlDataInfoDto.approverl_role_code = route_history.approverl_role_code
                approverlDataInfoDto.approverl_role_name = route_history.approverl_role_name
                approverlDataInfoDto.approverl_group_code = route_history.approverl_group_code
                approverlDataInfoDto.approverl_group_name = route_history.approverl_group_name
                approverlDataInfoDto.approverl_employee_code = route_history.approverl_employee_code
                approverlDataInfoDto.approverl_employee_name = route_history.approverl_employee_name
                approverlDataInfoDto.deputy_approverl_company_code = route_history.deputy_approverl_company_code
                approverlDataInfoDto.deputy_approverl_company_name = route_history.deputy_approverl_company_name
                approverlDataInfoDto.deputy_approverl_group_code = route_history.deputy_approverl_group_code
                approverlDataInfoDto.deputy_approverl_group_name = route_history.deputy_approverl_group_name
                approverlDataInfoDto.deputy_approverl_employee_code = route_history.deputy_approverl_employee_code
                approverlDataInfoDto.deputy_approverl_employee_name = route_history.deputy_approverl_employee_name
                approverlDataInfoDto.deputy_contents = route_history.deputy_contents
                approverlDataInfoDto.approval_function = route_history.function
                approverlDataInfoDto.reaching_date = route_history.reaching_date
                approverlDataInfoDto.process_date = route_history.process_date
                approverlDataInfoDto.activity_status = route_history.activity_status
                approverlDataInfoDto.approverl_comment = route_history.approverl_comment
                approverlDto.approverl_data_info_list.append(approverlDataInfoDto)

            # 申請明細オブジェクトを検索します。
            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, approverlDto.target_company_code, approverlDto.application_number)

            for activityObject in activityObjects:

                if (activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and approval.ApplicationObject.application_status != ApplicationStatus.DENIAL) or activityObject.activity_status == ActivityStatus.ARRIVAL or activityObject.activity_status == ActivityStatus.HOLD:  # [未処理]または[到着]または[保留]の場合

                    approverlDataInfoDto = ApproverlDataInfoDto()
                    approverlDataInfoDto.company_code = activityObject.company_code
                    approverlDataInfoDto.company_name = self.__get_company_name(session, activityObject.company_code)
                    approverlDataInfoDto.application_number = activityObject.application_number
                    approverlDataInfoDto.target_company_code = approval.ApplicationObject.target_company_code  # 対象者の会社コード
                    approverlDataInfoDto.target_company_name = self.__get_company_name(session, approval.ApplicationObject.target_company_code)  # 対象者の会社名
                    approverlDataInfoDto.target_group_code = approval.ApplicationObject.target_group_code  # 対象者の部署コード
                    approverlDataInfoDto.target_group_name = self.__get_group_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_group_code)  # 対象者の部署名
                    approverlDataInfoDto.target_employee_code = approval.ApplicationObject.target_employee_code  # 対象者の従業員番号
                    approverlDataInfoDto.target_employee_name = self.__get_employee_name(session, approval.ApplicationObject.target_company_code, approval.ApplicationObject.target_employee_code)  # 対象者の従業員名
                    approverlDataInfoDto.applicant_company_code = approval.ApplicationObject.applicant_company_code  # 申請者の会社コード
                    approverlDataInfoDto.applicant_company_name = self.__get_company_name(session, approval.ApplicationObject.applicant_company_code)  # 申請者の会社名
                    approverlDataInfoDto.applicant_group_code = approval.ApplicationObject.applicant_group_code  # 申請者の部署コード
                    approverlDataInfoDto.applicant_group_name = self.__get_group_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_group_code)  # 申請者の部署名
                    approverlDataInfoDto.applicant_employee_code = approval.ApplicationObject.applicant_employee_code  # 申請者の従業員番号
                    approverlDataInfoDto.applicant_employee_name = self.__get_employee_name(session, approval.ApplicationObject.applicant_company_code, approval.ApplicationObject.applicant_employee_code)  # 申請者の従業員名
                    approverlDataInfoDto.apply_date = approval.ApplicationObject.apply_date  # 申請日
                    approverlDataInfoDto.application_status = approval.ApplicationObject.application_status  # 申請書ステータス
                    approverlDataInfoDto.applicant_status = None  # 申請者ステータス
                    approverlDataInfoDto.route_type = activityObject.route_type
                    approverlDataInfoDto.route_number = activityObject.route_number
                    approverlDataInfoDto.approverl_company_code = activityObject.approverl_company_code
                    approverlDataInfoDto.approverl_company_name = self.__get_company_name(session, activityObject.approverl_company_code)
                    approverlDataInfoDto.approverl_role_code = activityObject.approverl_role_code

                    roleDao = RoleDao()
                    role = roleDao.find_ix_m_role(session, activityObject.approverl_company_code, activityObject.approverl_role_code)

                    if role is None:
                        approverlDataInfoDto.approverl_role_name = None
                    else:
                        approverlDataInfoDto.approverl_role_name = role.role_name

                    approverlDataInfoDto.approverl_group_code = activityObject.approverl_group_code
                    approverlDataInfoDto.approverl_group_name = self.__get_group_name(session, activityObject.approverl_company_code, activityObject.approverl_group_code)
                    approverlDataInfoDto.approverl_employee_code = activityObject.approverl_employee_code
                    approverlDataInfoDto.approverl_employee_name = self.__get_employee_name(session, activityObject.approverl_company_code, activityObject.approverl_employee_code)
                    approverlDataInfoDto.deputy_approverl_company_code = activityObject.deputy_approverl_company_code
                    approverlDataInfoDto.deputy_approverl_company_name = self.__get_company_name(session, activityObject.deputy_approverl_company_code)
                    approverlDataInfoDto.deputy_approverl_group_code = activityObject.deputy_approverl_group_code
                    approverlDataInfoDto.deputy_approverl_group_name = self.__get_group_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_group_code)
                    approverlDataInfoDto.deputy_approverl_employee_code = activityObject.deputy_approverl_employee_code
                    approverlDataInfoDto.deputy_approverl_employee_name = self.__get_employee_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_employee_code)
                    approverlDataInfoDto.deputy_contents = activityObject.deputy_contents
                    approverlDataInfoDto.approval_function = activityObject.function
                    approverlDataInfoDto.reaching_date = activityObject.reaching_date
                    approverlDataInfoDto.process_date = activityObject.process_date
                    approverlDataInfoDto.activity_status = activityObject.activity_status
                    approverlDataInfoDto.approverl_comment = activityObject.approverl_comment

                    approverlDto.approverl_data_info_list.append(approverlDataInfoDto)

            return approverlDto

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認画面の承認ボタン押下時

    [機能]
    承認処理を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        route_type : ルートタイプ
        route_number : ルート番号
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        deputy_approverl_company_code : 会社コード[代理承認者]
        deputy_approverl_group_code : 部署コード[代理承認者]
        deputy_approverl_employee_code : 従業員番号[代理承認者]
        approverl_comment : 承認者のコメント
        screen_mode : 画面モード

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def approve(self, session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, deputy_approverl_company_code, deputy_approverl_group_code, deputy_approverl_employee_code, approverl_comment, screen_mode):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if application_number is None:
                raise LaubeException('required application_number')

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            if route_type is None:
                raise LaubeException('required route_type')

            if route_number is None:
                raise LaubeException('required route_number')

            if screen_mode is None:
                raise LaubeException('required screen_mode')

            # 承認モード1　[差し戻し/保留/否認/承認]以外はエラー
            if screen_mode != ScreenMode.APPROVAL_MODE_1:
                raise LaubeException('unmatch screen_mode')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, company_code, application_number)

            if applicationObject is None:
                raise LaubeException(f'applicationObject record is missing. key={company_code},{application_number}')

            approverl_role_code_list = list()
            employeeGroupRoleDao = EmployeeGroupRoleDao()
            employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
            if employeeGroupRoles is None:
                pass
            else:
                for employeeGroupRole in employeeGroupRoles:
                    approverl_role_code_list.append(employeeGroupRole.role_code)

            dt = datetime.now()

            activityObjectDao = ActivityObjectDao()
            activityObject = activityObjectDao.find_activity_object(session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list)

            if activityObject is None:
                raise LaubeException('missing activityObject')

            activityObject = activityObject.ActivityObject

            if activityObject.activity_status != ActivityStatus.ARRIVAL and activityObject.activity_status != ActivityStatus.HOLD:  # 承認者のステータスが[到着]と[保留]以外の場合
                return None  # 同時につかんだ場合に発生するため、処理をしないで終わるよう修正

            # 代理承認か判定します。
            is_deputy = False
            if deputy_approverl_company_code is not None and deputy_approverl_group_code is not None and deputy_approverl_employee_code is not None:
                is_deputy = True
            else:
                if deputy_approverl_company_code is None and deputy_approverl_group_code is None and deputy_approverl_employee_code is None:
                    is_deputy = False
                else:
                    raise LaubeException('required deputy_approverl_employee_code')

            if is_deputy:
                # 承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報を設定します。
                activityObject.deputy_approverl_company_code = deputy_approverl_company_code
                activityObject.deputy_approverl_group_code = deputy_approverl_group_code
                activityObject.deputy_approverl_employee_code = deputy_approverl_employee_code
            else:
                # 承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報をクリアします。
                activityObject.deputy_approverl_company_code = None
                activityObject.deputy_approverl_group_code = None
                activityObject.deputy_approverl_employee_code = None

            activityObject.activity_status = ActivityStatus.AUTHORIZER_APPROVAL  # 承認
            activityObject.approverl_comment = approverl_comment  # 承認者のコメント
            activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日
            activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
            activityObject.update_employee_code = approverl_employee_code
            activityObject.update_count = activityObject.update_count + 1

            # 申請書履歴オブジェクトを更新します。
            self.__add_history(session, applicationObject, activityObject, None)

            session.flush()

            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            # 同一ルートタイプ、同一ルート番号の承認者が複数いた場合、承認に携わらなかった承認者を削除します。
            for activityObject in activityObjects:
                if activityObject.route_type == route_type and activityObject.route_number == route_number:
                    if activityObject.activity_status != ActivityStatus.AUTHORIZER_APPROVAL:
                        activityObjectDao.delete(session, activityObject.id)

            # 次の承認者を[到着]に変更します。最終承認者の場合は申請オブジェクトを承認済にします。
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            is_finish = True  # 最終承認済　判定用
            w_route_type = None
            w_route_number = None
            for activityObject in activityObjects:
                if activityObject.route_type == route_type and activityObject.route_number == route_number:  # 自分自身を読み飛ばします。
                    continue
                else:
                    if activityObject.route_type == w_route_type and activityObject.route_number == w_route_number:
                        activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                        activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日

                    else:
                        if w_route_type is not None and w_route_number is not None:
                            break

                        if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and activityObject.function == ApprovalFunction.EXAMINATION:  # 承認
                            is_finish = False
                            activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                            activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                            w_route_type = activityObject.route_type  # 比較条件を[到着]の申請明細に変更(並列対応)
                            w_route_number = activityObject.route_number  # 比較条件を[到着]の申請明細に変更(並列対応)

                        else:
                            if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and activityObject.function == ApprovalFunction.FUNCTION_CONFIRMATION:  # 確認
                                activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                                activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                                w_route_type = activityObject.route_type  # 比較条件を[到着]の申請明細に変更(並列対応)
                                w_route_number = activityObject.route_number  # 比較条件を[到着]の申請明細に変更(並列対応)

                            else:
                                if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and activityObject.function == ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL:  # 自動承認
                                    activityObject.activity_status = ActivityStatus.AUTHORIZER_AUTOMATIC_APPROVAL  # [自動承認]
                                    activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                                    activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日

                                    # 申請書履歴オブジェクトを更新します。
                                    self.__add_history(session, applicationObject, activityObject, None)

                                    w_route_type = activityObject.route_type  # 比較条件を[到着]の申請明細に変更(自動承認の次を検索)
                                    w_route_number = activityObject.route_number  # 比較条件を[到着]の申請明細に変更(自動承認の次を検索)
                                else:
                                    pass

            if is_finish:  # 最終承認だった場合、[申請書ステータス]を[承認]に変更します。 ※[確認]については考慮しません。[承認画面の機能]が[承認]になっている全ての承認者が承認したら最終承認となります。
                applicationObject.application_status = ApplicationStatus.APPROVED  # [申請書のステータス]を[承認]に変更します。
                applicationObject.approval_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 承認日

            return is_finish

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    停滞画面の強制承認ボタン押下時
    ※到着と保留以外は処理できません。

    [機能]
    承認処理を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        route_type : ルートタイプ
        route_number : ルート番号
        approverl_company_code : 強制承認ボタンを押下した承認者の会社コード[承認者]
        approverl_group_code : 強制承認ボタンを押下した承認者の部署コード[承認者]
        approverl_employee_code : 強制承認ボタンを押下した承認者の従業員番号[承認者]
        approverl_comment : 強制承認ボタンを押下した承認者の承認者のコメント
        screen_mode : 画面モード

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def authorizer_forced_approval(self, session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_comment, screen_mode):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if application_number is None:
                raise LaubeException('required application_number')

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            if route_type is None:
                raise LaubeException('required route_type')

            if route_number is None:
                raise LaubeException('required route_number')

            if screen_mode is None:
                raise LaubeException('required screen_mode')

            # 承認モード4　[強制承認]以外はエラー
            if screen_mode != ScreenMode.APPROVAL_MODE_4:
                raise LaubeException('unmatch screen_mode')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, company_code, application_number)

            if applicationObject is None:
                raise LaubeException(f'applicationObject record is missing. key={company_code},{application_number}')

            dt = datetime.now()

            activityObjectDao = ActivityObjectDao()
            activityObject = activityObjectDao.find_activity_object_authorizer_forced_approval(session, company_code, application_number, route_type, route_number)

            if activityObject is None:
                raise LaubeException('missing activityObject')

            activityObject = activityObject.ActivityObject

            if ApprovalFunction.EXAMINATION != activityObject.function:  # 承認画面の機能が[審査]以外の場合
                raise LaubeException('function error')

            if activityObject.activity_status != ActivityStatus.ARRIVAL and activityObject.activity_status != ActivityStatus.HOLD:  # 承認者のステータスが[到着]と[保留]以外の場合
                raise LaubeException('status error activity_status')

            # 承認時は、利用権限コードはクリアし承認者の情報に置換します。※強制承認は代理承認できません。[仕様]

            employeeDao = EmployeeDao()
            employee = employeeDao.find_ix_m_employee(session, company_code, approverl_employee_code)

            if employee is None:
                raise LaubeException('employee is nothing')

            max_route_number = activityObjectDao.get_max_route_number(session, company_code, application_number, route_type)

            activityObject = ActivityObject()
            activityObject.company_code = company_code
            activityObject.application_number = application_number
            activityObject.route_type = route_type
            activityObject.route_number = max_route_number
            activityObject.approverl_company_code = approverl_company_code
            activityObject.approverl_role_code = None
            activityObject.approverl_group_code = approverl_group_code
            activityObject.approverl_employee_code = approverl_employee_code
            activityObject.deputy_approverl_company_code = None
            activityObject.deputy_approverl_group_code = None
            activityObject.deputy_approverl_employee_code = None
            activityObject.deputy_contents = None
            activityObject.function = ApprovalFunction.AUTHORIZER_FORCED_APPROVAL
            activityObject.reaching_date = activityObject.reaching_date

            dt = datetime.now()

            activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')
            activityObject.activity_status = ActivityStatus.AUTHORIZER_FORCED_APPROVAL
            activityObject.approverl_comment = '一定期間の間、承認者[' + employee.employee_name + ']は承認を停滞させていた為、強制承認を行いました。 強制承認の理由:' + approverl_comment  # 承認者のコメント
            activityObject.create_employee_code = approverl_employee_code
            activityObject.update_employee_code = approverl_employee_code
            activityObject.update_count = 1
            activityObjectDao.add(session, activityObject)

            session.flush()

            # 申請書履歴オブジェクトを更新します。
            self.__add_history(session, applicationObject, activityObject, None)

            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            # [未処理]または[到着]または[保留]の承認者の [承認画面の機能]を[確認]に変更
            for activityObject in activityObjects:
                if activityObject.function == ApprovalFunction.EXAMINATION:  # [承認画面の機能]が[審査]
                    if activityObject.activity_status == ActivityStatus.AUTHORIZER_HIKE_APPROVAL:
                        break
                    else:
                        if (activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and applicationObject.application_status != ApplicationStatus.DENIAL) or activityObject.activity_status == ActivityStatus.ARRIVAL or activityObject.activity_status == ActivityStatus.HOLD:  # [未処理]または[到着]または[保留]の場合
                            activityObject.function = ApprovalFunction.FUNCTION_CONFIRMATION  # [承認画面の機能]を[確認]に変更

            applicationObject.application_status = ApplicationStatus.APPROVED  # [申請書のステータス]を[承認]に変更します。
            applicationObject.approval_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 承認日

            session.flush()

            return True

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認画面の否認ボタン押下時

    [機能]
    否認処理を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        route_type : ルートタイプ
        route_number : ルート番号
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        deputy_approverl_company_code : 会社コード[代理承認者]
        deputy_approverl_group_code : 部署コード[代理承認者]
        deputy_approverl_employee_code : 従業員番号[代理承認者]
        approverl_comment : 承認者のコメント
        screen_mode : 画面モード

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def denial(self, session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, deputy_approverl_company_code, deputy_approverl_group_code, deputy_approverl_employee_code, approverl_comment, screen_mode):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if application_number is None:
                raise LaubeException('required application_number')

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            if route_type is None:
                raise LaubeException('required route_type')

            if route_number is None:
                raise LaubeException('required route_number')

            if screen_mode is None:
                raise LaubeException('required screen_mode')

            # 承認モード1　[差し戻し/保留/否認/承認]以外はエラー
            if screen_mode != ScreenMode.APPROVAL_MODE_1:
                raise LaubeException('unmatch screen_mode')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, company_code, application_number)

            if applicationObject is None:
                raise LaubeException(f'applicationObject record is missing. key={company_code},{application_number}')

            approverl_role_code_list = list()
            employeeGroupRoleDao = EmployeeGroupRoleDao()
            employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
            if employeeGroupRoles is None:
                pass
            else:
                for employeeGroupRole in employeeGroupRoles:
                    approverl_role_code_list.append(employeeGroupRole.role_code)

            dt = datetime.now()

            activityObjectDao = ActivityObjectDao()
            activityObject = activityObjectDao.find_activity_object(session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list)

            if activityObject is None:
                raise LaubeException('missing activityObject')

            activityObject = activityObject.ActivityObject

            if activityObject.activity_status != ActivityStatus.ARRIVAL and activityObject.activity_status != ActivityStatus.HOLD:  # 承認者のステータスが[到着]と[保留]以外の場合
                raise LaubeException('status error activity_status')

            # 申請者承認か判定します。
            is_deputy = False
            if deputy_approverl_company_code is not None and deputy_approverl_group_code is not None and deputy_approverl_employee_code is not None:
                is_deputy = True
            else:
                if deputy_approverl_company_code is None and deputy_approverl_group_code is None and deputy_approverl_employee_code is None:
                    is_deputy = False
                else:
                    raise LaubeException('required deputy_approverl_employee_code')

            if is_deputy:
                # 否認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報を設定します。
                activityObject.deputy_approverl_company_code = deputy_approverl_company_code
                activityObject.deputy_approverl_group_code = deputy_approverl_group_code
                activityObject.deputy_approverl_employee_code = deputy_approverl_employee_code
            else:
                # 否認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報をクリアします。
                activityObject.deputy_approverl_company_code = None
                activityObject.deputy_approverl_group_code = None
                activityObject.deputy_approverl_employee_code = None

            activityObject.activity_status = ActivityStatus.AUTHORIZER_DENIAL  # 否認
            activityObject.approverl_comment = approverl_comment  # 承認者のコメント
            activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日
            activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
            activityObject.update_employee_code = approverl_employee_code
            activityObject.update_count = activityObject.update_count + 1

            # 申請書履歴オブジェクトを更新します。
            self.__add_history(session, applicationObject, activityObject, None)

            session.flush()

            # [未着]の承認者を全て削除します。
            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            for activityObject in activityObjects:
                if ActivityStatus.AUTHORIZER_UNTREATED == activityObject.activity_status:  # 未処理の場合
                    activityObjectDao.delete(session, activityObject.id)

            applicationObject.application_status = ApplicationStatus.DENIAL  # [申請書のステータス]を[否認]に変更します。

            return True

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認画面の保留ボタン押下時

    [機能]
    保留処理を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        route_type : ルートタイプ
        route_number : ルート番号
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        deputy_approverl_company_code : 会社コード[代理承認者]
        deputy_approverl_group_code : 部署コード[代理承認者]
        deputy_approverl_employee_code : 従業員番号[代理承認者]
        approverl_comment : 承認者のコメント
        screen_mode : 画面モード

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def hold(self, session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, deputy_approverl_company_code, deputy_approverl_group_code, deputy_approverl_employee_code, approverl_comment, screen_mode):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if application_number is None:
                raise LaubeException('required application_number')

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            if route_type is None:
                raise LaubeException('required route_type')

            if route_number is None:
                raise LaubeException('required route_number')

            if screen_mode is None:
                raise LaubeException('required screen_mode')

            # 承認モード1　[差し戻し/保留/否認/承認]以外はエラー
            if screen_mode != ScreenMode.APPROVAL_MODE_1:
                raise LaubeException('unmatch screen_mode')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, company_code, application_number)

            if applicationObject is None:
                raise LaubeException(f'applicationObject record is missing. key={company_code},{application_number}')

            approverl_role_code_list = list()
            employeeGroupRoleDao = EmployeeGroupRoleDao()
            employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
            if employeeGroupRoles is None:
                pass
            else:
                for employeeGroupRole in employeeGroupRoles:
                    approverl_role_code_list.append(employeeGroupRole.role_code)

            dt = datetime.now()

            activityObjectDao = ActivityObjectDao()
            activityObject = activityObjectDao.find_activity_object(session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list)

            if activityObject is None:
                raise LaubeException('missing activityObject')

            activityObject = activityObject.ActivityObject

            if activityObject.activity_status != ActivityStatus.ARRIVAL and activityObject.activity_status != ActivityStatus.HOLD:  # 承認者のステータスが[到着]と[保留]以外の場合
                raise LaubeException('status error activity_status')

            # 申請者承認か判定します。
            is_deputy = False
            if deputy_approverl_company_code is not None and deputy_approverl_group_code is not None and deputy_approverl_employee_code is not None:
                is_deputy = True
            else:
                if deputy_approverl_company_code is None and deputy_approverl_group_code is None and deputy_approverl_employee_code is None:
                    is_deputy = False
                else:
                    raise LaubeException('required deputy_approverl_employee_code')

            if is_deputy:
                # 保留時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報を設定します。
                activityObject.deputy_approverl_company_code = deputy_approverl_company_code
                activityObject.deputy_approverl_group_code = deputy_approverl_group_code
                activityObject.deputy_approverl_employee_code = deputy_approverl_employee_code
            else:
                # 保留時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報をクリアします。
                activityObject.deputy_approverl_company_code = None
                activityObject.deputy_approverl_group_code = None
                activityObject.deputy_approverl_employee_code = None

            activityObject.activity_status = ActivityStatus.HOLD  # 保留
            activityObject.approverl_comment = approverl_comment  # 承認者のコメント
            activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日
            activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
            activityObject.update_employee_code = approverl_employee_code
            activityObject.update_count = activityObject.update_count + 1

            session.flush()

            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            # 同一ルートタイプ、同一ルート番号の承認者が複数いた場合、承認に携わらなかった承認者を削除します。
            for activityObject in activityObjects:
                if activityObject.route_type == route_type and activityObject.route_number == route_number:
                    if activityObject.activity_status != ActivityStatus.HOLD:
                        activityObjectDao.delete(session, activityObject.id)

            return True

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認画面の差し戻しボタン押下時

    [機能]
    差し戻し処理を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        route_type : ルートタイプ
        route_number : ルート番号
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        deputy_approverl_company_code : 会社コード[代理承認者]
        deputy_approverl_group_code : 部署コード[代理承認者]
        deputy_approverl_employee_code : 従業員番号[代理承認者]
        approverl_comment : 承認者のコメント
        screen_mode : 画面モード

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def with_drawal(self, session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, deputy_approverl_company_code, deputy_approverl_group_code, deputy_approverl_employee_code, approverl_comment, screen_mode):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if application_number is None:
                raise LaubeException('required application_number')

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            if route_type is None:
                raise LaubeException('required route_type')

            if route_number is None:
                raise LaubeException('required route_number')

            if screen_mode is None:
                raise LaubeException('required screen_mode')

            # 承認モード1　[差し戻し/保留/否認/承認]以外はエラー
            if screen_mode != ScreenMode.APPROVAL_MODE_1:
                raise LaubeException('unmatch screen_mode')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, company_code, application_number)

            if applicationObject is None:
                raise LaubeException(f'applicationObject record is missing. key={company_code},{application_number}')

            approverl_role_code_list = list()
            employeeGroupRoleDao = EmployeeGroupRoleDao()
            employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
            if employeeGroupRoles is None:
                pass
            else:
                for employeeGroupRole in employeeGroupRoles:
                    approverl_role_code_list.append(employeeGroupRole.role_code)

            dt = datetime.now()

            activityObjectDao = ActivityObjectDao()
            activityObject = activityObjectDao.find_activity_object(session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list)

            if activityObject is None:
                raise LaubeException('missing activityObject')

            activityObject = activityObject.ActivityObject

            if activityObject.activity_status != ActivityStatus.ARRIVAL and activityObject.activity_status != ActivityStatus.HOLD:  # 承認者のステータスが[到着]と[保留]以外の場合
                raise LaubeException('status error activity_status')

            # 代理承認か判定します。
            is_deputy = False
            if deputy_approverl_company_code is not None and deputy_approverl_group_code is not None and deputy_approverl_employee_code is not None:
                is_deputy = True
            else:
                if deputy_approverl_company_code is None and deputy_approverl_group_code is None and deputy_approverl_employee_code is None:
                    is_deputy = False
                else:
                    raise LaubeException('required deputy_approverl_employee_code')

            if is_deputy:
                # 承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報を設定します。
                activityObject.deputy_approverl_company_code = deputy_approverl_company_code
                activityObject.deputy_approverl_group_code = deputy_approverl_group_code
                activityObject.deputy_approverl_employee_code = deputy_approverl_employee_code
            else:
                # 承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報をクリアします。
                activityObject.deputy_approverl_company_code = None
                activityObject.deputy_approverl_group_code = None
                activityObject.deputy_approverl_employee_code = None

            activityObject.activity_status = ActivityStatus.WITH_DRAWAL  # 差し戻し
            activityObject.approverl_comment = approverl_comment  # 承認者のコメント
            activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日
            activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
            activityObject.update_employee_code = approverl_employee_code
            activityObject.update_count = activityObject.update_count + 1

            # 申請書履歴オブジェクトを更新します。
            self.__add_history(session, applicationObject, activityObject, None)

            session.flush()

            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            # 同一ルートタイプ、同一ルート番号の承認者が複数いた場合、承認に携わらなかった承認者を削除します。
            # ※差し戻しした場合、並列承認者は全て削除し、再度、審査依頼がきた場合は「差し戻し」をした承認者に届くようにします。
            for activityObject in activityObjects:
                if activityObject.route_type == route_type and activityObject.route_number == route_number:
                    if activityObject.activity_status != ActivityStatus.WITH_DRAWAL:
                        activityObjectDao.delete(session, activityObject.id)

            session.flush()

            # 差し戻ししたので直前の状態に戻します。

            activityObjectDao = ActivityObjectDao()
            activityObject = activityObjectDao.find_activity_object(session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list)

            if activityObject is None:
                raise LaubeException('missing activityObject')

            activityObject = activityObject.ActivityObject

            if activityObject.activity_status != ActivityStatus.WITH_DRAWAL:  # 承認者のステータスが[差し戻し]以外の場合
                raise LaubeException('status error activity_status')

            # 承認時は、利用権限コードはクリアし承認者の情報に置換します。
            activityObject.approverl_company_code = approverl_company_code
            activityObject.approverl_role_code = None
            activityObject.approverl_group_code = approverl_group_code
            activityObject.approverl_employee_code = approverl_employee_code
            # 代理承認者の情報を設定します。
            activityObject.deputy_approverl_company_code = None
            activityObject.deputy_approverl_group_code = None
            activityObject.deputy_approverl_employee_code = None

            activityObject.activity_status = ActivityStatus.AUTHORIZER_UNTREATED  # 未処理
            activityObject.approverl_comment = None  # 承認者のコメント
            activityObject.process_date = None  # 処理日
            activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
            activityObject.update_employee_code = approverl_employee_code
            activityObject.update_count = activityObject.update_count + 1

            if route_number == 1:  # 差し戻し先が申請者の場合
                applicationObject.application_status = ApplicationStatus.WITH_DRAWAL  # 差し戻し
                pass

            else:
                w_route_type = activityObject.route_type
                w_route_number = route_number - 1

                # 直前の承認者を[到着]に変更します。
                activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
                if activityObjects is None:
                    raise LaubeException('nothing activityObjects.')

                for activityObject in activityObjects:
                    if activityObject.route_type == w_route_type and activityObject.route_number == w_route_number:  # 直前の承認者の場合
                        if activityObject.function == ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL:  # [自動承認]の場合
                            if w_route_number == 1:
                                applicationObject.application_status = ApplicationStatus.WITH_DRAWAL  # 差し戻し
                                break
                            else:
                                w_route_number -= 1
                                activityObject.activity_status = ActivityStatus.AUTHORIZER_UNTREATED  # 未処理
                                activityObject.approverl_comment = None  # 承認者のコメント
                                activityObject.reaching_date = None  # 到着日
                                activityObject.process_date = None  # 処理日
                                activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                                activityObject.update_employee_code = approverl_employee_code
                                activityObject.update_count = activityObject.update_count + 1
                                continue
                        else:
                            activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                            activityObject.approverl_comment = None  # 承認者のコメント
                            activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                            activityObject.process_date = None  # 処理日
                            activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
                            activityObject.update_employee_code = approverl_employee_code
                            activityObject.update_count = activityObject.update_count + 1
                            break
                    else:
                        pass

            session.flush()
            return True

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認画面の先取り承認ボタン押下時

    [機能]
    先取り承認処理を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        route_type : ルートタイプ
        route_number : ルート番号
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        deputy_approverl_company_code : 会社コード[代理承認者]
        deputy_approverl_group_code : 部署コード[代理承認者]
        deputy_approverl_employee_code : 従業員番号[代理承認者]
        approverl_comment : 承認者のコメント
        screen_mode : 画面モード

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def anticipating_approve(self, session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, deputy_approverl_company_code, deputy_approverl_group_code, deputy_approverl_employee_code, approverl_comment, screen_mode):

        try:
            if not session:
                raise LaubeException(self.E001)

            # 引数を確認します
            if not company_code:
                raise LaubeException('required company_code')

            if application_number is None:
                raise LaubeException('required application_number')

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            if route_type is None:
                raise LaubeException('required route_type')

            if route_number is None:
                raise LaubeException('required route_number')

            if screen_mode is None:
                raise LaubeException('required screen_mode')

            # 承認モード3　[先取り承認/引き上げ承認]以外はエラー
            if screen_mode != ScreenMode.APPROVAL_MODE_3:
                raise LaubeException('unmatch screen_mode')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, company_code, application_number)

            if applicationObject is None:
                raise LaubeException(f'applicationObject record is missing. key={company_code},{application_number}')

            approverl_role_code_list = list()
            employeeGroupRoleDao = EmployeeGroupRoleDao()
            employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
            if employeeGroupRoles is None:
                pass
            else:
                for employeeGroupRole in employeeGroupRoles:
                    approverl_role_code_list.append(employeeGroupRole.role_code)

            dt = datetime.now()

            activityObjectDao = ActivityObjectDao()
            activityObject = activityObjectDao.find_activity_object(session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list)

            if activityObject is None:
                raise LaubeException('missing activityObject')

            activityObject = activityObject.ActivityObject

            if activityObject.activity_status != ActivityStatus.AUTHORIZER_UNTREATED:  # 承認者のステータスが[未処理]以外の場合
                raise LaubeException('status error activity_status')

            # 申請者承認か判定します。
            is_deputy = False
            if deputy_approverl_company_code is not None and deputy_approverl_group_code is not None and deputy_approverl_employee_code is not None:
                is_deputy = True
            else:
                if deputy_approverl_company_code is None and deputy_approverl_group_code is None and deputy_approverl_employee_code is None:
                    is_deputy = False
                else:
                    raise LaubeException('required deputy_approverl_employee_code')

            if is_deputy:
                # 先取り承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報を設定します。
                activityObject.deputy_approverl_company_code = deputy_approverl_company_code
                activityObject.deputy_approverl_group_code = deputy_approverl_group_code
                activityObject.deputy_approverl_employee_code = deputy_approverl_employee_code
            else:
                # 先取り承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報をクリアします。
                activityObject.deputy_approverl_company_code = None
                activityObject.deputy_approverl_group_code = None
                activityObject.deputy_approverl_employee_code = None

            activityObject.activity_status = ActivityStatus.AUTHORIZER_APPROVAL  # 承認
            activityObject.approverl_comment = approverl_comment  # 承認者のコメント
            activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到達日
            activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日
            activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
            activityObject.update_employee_code = approverl_employee_code
            activityObject.update_count = activityObject.update_count + 1

            # 申請書履歴オブジェクトを更新します。
            self.__add_history(session, applicationObject, activityObject, None)

            session.flush()

            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            # 同一ルートタイプ、同一ルート番号の承認者が複数いた場合、承認に携わらなかった承認者を削除します。
            for activityObject in activityObjects:
                if activityObject.route_type == route_type and activityObject.route_number == route_number:
                    if activityObject.activity_status != ActivityStatus.AUTHORIZER_APPROVAL:
                        activityObjectDao.delete(session, activityObject.id)

            session.flush()

            # 最終承認済がチェック
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            is_finish = True  # 最終承認済　判定用
            for activityObject in activityObjects:
                if activityObject.function == ApprovalFunction.EXAMINATION:  # [承認画面の機能]が[審査]
                    if (activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and applicationObject.application_status != ApplicationStatus.DENIAL) or activityObject.activity_status == ActivityStatus.ARRIVAL or activityObject.activity_status == ActivityStatus.HOLD:  # [未処理]または[到着]または[保留]の場合
                        is_finish = False
                        break
                else:
                    pass

            if is_finish:  # 最終承認だった場合、[申請書ステータス]を[承認]に変更します。 ※[確認]については考慮しません。[承認画面の機能]が[承認]になっている全ての承認者が承認したら最終承認となります。
                applicationObject.application_status = ApplicationStatus.APPROVED  # [申請書のステータス]を[承認]に変更します。
                applicationObject.approval_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 承認日

            return is_finish

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認画面の引き上げ承認ボタン押下時

    [機能]
    引き上げ承認処理を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        route_type : ルートタイプ
        route_number : ルート番号
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        deputy_approverl_company_code : 会社コード[代理承認者]
        deputy_approverl_group_code : 部署コード[代理承認者]
        deputy_approverl_employee_code : 従業員番号[代理承認者]
        approverl_comment : 承認者のコメント
        screen_mode : 画面モード

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def hike_approve(self, session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, deputy_approverl_company_code, deputy_approverl_group_code, deputy_approverl_employee_code, approverl_comment, screen_mode):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if application_number is None:
                raise LaubeException('required application_number')

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            if route_type is None:
                raise LaubeException('required route_type')

            if route_number is None:
                raise LaubeException('required route_number')

            if screen_mode is None:
                raise LaubeException('required screen_mode')

            # 承認モード3　[先取り承認/引き上げ承認]以外はエラー
            if screen_mode != ScreenMode.APPROVAL_MODE_3:
                raise LaubeException('unmatch screen_mode')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, company_code, application_number)

            if applicationObject is None:
                raise LaubeException(f'applicationObject record is missing. key={company_code},{application_number}')

            approverl_role_code_list = list()
            employeeGroupRoleDao = EmployeeGroupRoleDao()
            employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
            if employeeGroupRoles is None:
                pass
            else:
                for employeeGroupRole in employeeGroupRoles:
                    approverl_role_code_list.append(employeeGroupRole.role_code)

            dt = datetime.now()

            activityObjectDao = ActivityObjectDao()
            activityObject = activityObjectDao.find_activity_object(session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list)

            if activityObject is None:
                raise LaubeException('missing activityObject')

            activityObject = activityObject.ActivityObject

            if activityObject.activity_status != ActivityStatus.AUTHORIZER_UNTREATED:  # 承認者のステータスが[未処理]以外の場合
                raise LaubeException('status error activity_status')

            # 申請者承認か判定します。
            is_deputy = False
            if deputy_approverl_company_code is not None and deputy_approverl_group_code is not None and deputy_approverl_employee_code is not None:
                is_deputy = True
            else:
                if deputy_approverl_company_code is None and deputy_approverl_group_code is None and deputy_approverl_employee_code is None:
                    is_deputy = False
                else:
                    raise LaubeException('required deputy_approverl_employee_code')

            if is_deputy:
                # 承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報を設定します。
                activityObject.deputy_approverl_company_code = deputy_approverl_company_code
                activityObject.deputy_approverl_group_code = deputy_approverl_group_code
                activityObject.deputy_approverl_employee_code = deputy_approverl_employee_code
            else:
                # 承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報をクリアします。
                activityObject.deputy_approverl_company_code = None
                activityObject.deputy_approverl_group_code = None
                activityObject.deputy_approverl_employee_code = None

            activityObject.activity_status = ActivityStatus.AUTHORIZER_HIKE_APPROVAL  # 引き上げ承認
            activityObject.approverl_comment = approverl_comment  # 承認者のコメント
            activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
            activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日
            activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
            activityObject.update_employee_code = approverl_employee_code
            activityObject.update_count = activityObject.update_count + 1

            # 申請書履歴オブジェクトを更新します。
            self.__add_history(session, applicationObject, activityObject, None)

            session.flush()

            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            # 同一ルートタイプ、同一ルート番号の承認者が複数いた場合、承認に携わらなかった承認者を削除します。
            for activityObject in activityObjects:
                if activityObject.route_type == route_type and activityObject.route_number == route_number:
                    if activityObject.activity_status != ActivityStatus.AUTHORIZER_HIKE_APPROVAL:
                        activityObjectDao.delete(session, activityObject.id)

            session.flush()

            # 下位の承認者の [承認画面の機能]を[確認]に変更
            for activityObject in activityObjects:
                if activityObject.function == ApprovalFunction.EXAMINATION:  # [承認画面の機能]が[審査]
                    if activityObject.activity_status == ActivityStatus.AUTHORIZER_HIKE_APPROVAL:
                        break
                    else:
                        if (activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and applicationObject.application_status != ApplicationStatus.DENIAL):
                            activityObject.function = ApprovalFunction.FUNCTION_CONFIRMATION  # [承認画面の機能]を[確認]に変更
                            activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                            activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日

                        elif activityObject.activity_status == ActivityStatus.ARRIVAL:
                            activityObject.function = ApprovalFunction.FUNCTION_CONFIRMATION  # [承認画面の機能]を[確認]に変更

                        elif activityObject.activity_status == ActivityStatus.HOLD:
                            activityObject.function = ApprovalFunction.FUNCTION_CONFIRMATION  # [承認画面の機能]を[確認]に変更

            session.flush()

            # 最終承認済がチェック
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            is_finish = True  # 最終承認済　判定用
            w_route_type = None
            w_route_number = None

            for activityObject in activityObjects:
                if activityObject.route_type == route_type and activityObject.route_number == route_number:  # 自分自身を読み飛ばします。
                    continue
                else:
                    if activityObject.route_type == w_route_type and activityObject.route_number == w_route_number:
                        activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                        activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日

                    else:
                        if w_route_type is not None and w_route_number is not None:
                            break

                        if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and activityObject.function == ApprovalFunction.EXAMINATION:  # 承認
                            is_finish = False
                            activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                            activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                            w_route_type = activityObject.route_type  # 比較条件を[到着]の申請明細に変更(並列対応)
                            w_route_number = activityObject.route_number  # 比較条件を[到着]の申請明細に変更(並列対応)

                        else:
                            if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and activityObject.function == ApprovalFunction.FUNCTION_CONFIRMATION:  # 確認
                                activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                                activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                                w_route_type = activityObject.route_type  # 比較条件を[到着]の申請明細に変更(並列対応)
                                w_route_number = activityObject.route_number  # 比較条件を[到着]の申請明細に変更(並列対応)

                            else:
                                if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and activityObject.function == ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL:  # 自動承認
                                    activityObject.activity_status = ActivityStatus.AUTHORIZER_AUTOMATIC_APPROVAL  # [自動承認]
                                    activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                                    activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日

                                    # 申請書履歴オブジェクトを更新します。
                                    self.__add_history(session, applicationObject, activityObject, None)

                                    w_route_type = activityObject.route_type  # 比較条件を[到着]の申請明細に変更(自動承認の次を検索)
                                    w_route_number = activityObject.route_number  # 比較条件を[到着]の申請明細に変更(自動承認の次を検索)
                                else:
                                    pass

            if is_finish:  # 最終承認だった場合、[申請書ステータス]を[承認]に変更します。 ※[確認]については考慮しません。[承認画面の機能]が[承認]になっている全ての承認者が承認したら最終承認となります。
                applicationObject.application_status = ApplicationStatus.APPROVED  # [申請書のステータス]を[承認]に変更します。
                applicationObject.approval_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 承認日

            return is_finish

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    承認画面の確認ボタン押下時

    [機能]
    確認処理を行います。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_number : 申請番号
        route_type : ルートタイプ
        route_number : ルート番号
        approverl_company_code : 会社コード[承認者]
        approverl_group_code : 部署コード[承認者]
        approverl_employee_code : 従業員番号[承認者]
        deputy_approverl_company_code : 会社コード[代理承認者]
        deputy_approverl_group_code : 部署コード[代理承認者]
        deputy_approverl_employee_code : 従業員番号[代理承認者]
        approverl_comment : 承認者のコメント
        screen_mode : 画面モード

    Returns:
        なし

    Raises:
        LaubeException : Laube例外
    """
    def confirmation(self, session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, deputy_approverl_company_code, deputy_approverl_group_code, deputy_approverl_employee_code, approverl_comment, screen_mode):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                raise LaubeException('required company_code')

            if application_number is None:
                raise LaubeException('required application_number')

            if not approverl_company_code:
                raise LaubeException('required approverl_company_code')

            if route_type is None:
                raise LaubeException('required route_type')

            if route_number is None:
                raise LaubeException('required route_number')

            if screen_mode is None:
                raise LaubeException('required screen_mode')

            # CONFIRMATION_MODE 確認モード [確認]以外はエラー
            if screen_mode != ScreenMode.CONFIRMATION_MODE:
                raise LaubeException('unmatch screen_mode')

            # データベースのレコードを最初に取得します。[高速化対応]
            self.__get_database(session, company_code)

            applicationObjectDao = ApplicationObjectDao()
            applicationObject = applicationObjectDao.find_ix_t_application_object(session, company_code, application_number)

            if applicationObject is None:
                raise LaubeException(f'applicationObject record is missing. key={company_code},{application_number}')

            approverl_role_code_list = list()
            employeeGroupRoleDao = EmployeeGroupRoleDao()
            employeeGroupRoles = employeeGroupRoleDao.find_all_company_code_employee_code_group_code(session, approverl_company_code, approverl_employee_code, approverl_group_code)
            if employeeGroupRoles is None:
                pass
            else:
                for employeeGroupRole in employeeGroupRoles:
                    approverl_role_code_list.append(employeeGroupRole.role_code)

            dt = datetime.now()

            activityObjectDao = ActivityObjectDao()
            activityObject = activityObjectDao.find_activity_object(session, company_code, application_number, route_type, route_number, approverl_company_code, approverl_group_code, approverl_employee_code, approverl_role_code_list)

            if activityObject is None:
                raise LaubeException('missing activityObject')

            activityObject = activityObject.ActivityObject

            if activityObject.activity_status != ActivityStatus.ARRIVAL and activityObject.activity_status != ActivityStatus.HOLD:  # 承認者のステータスが[到着]と[保留]以外の場合
                raise LaubeException('status error activity_status')

            # 申請者承認か判定します。
            is_deputy = False
            if deputy_approverl_company_code is not None and deputy_approverl_group_code is not None and deputy_approverl_employee_code is not None:
                is_deputy = True
            else:
                if deputy_approverl_company_code is None and deputy_approverl_group_code is None and deputy_approverl_employee_code is None:
                    is_deputy = False
                else:
                    raise LaubeException('required deputy_approverl_employee_code')

            if is_deputy:
                # 承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報を設定します。
                activityObject.deputy_approverl_company_code = deputy_approverl_company_code
                activityObject.deputy_approverl_group_code = deputy_approverl_group_code
                activityObject.deputy_approverl_employee_code = deputy_approverl_employee_code
            else:
                # 承認時は、利用権限コードはクリアし承認者の情報に置換します。
                activityObject.approverl_company_code = approverl_company_code
                activityObject.approverl_role_code = None
                activityObject.approverl_group_code = approverl_group_code
                activityObject.approverl_employee_code = approverl_employee_code
                # 代理承認者の情報をクリアします。
                activityObject.deputy_approverl_company_code = None
                activityObject.deputy_approverl_group_code = None
                activityObject.deputy_approverl_employee_code = None

            activityObject.activity_status = ActivityStatus.AUTHORIZER_CONFIRMATION  # 確認
            activityObject.approverl_comment = approverl_comment  # 承認者のコメント
            activityObject.process_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 処理日
            activityObject.update_date = dt.strftime('%Y/%m/%d %H:%M:%S')
            activityObject.update_employee_code = approverl_employee_code
            activityObject.update_count = activityObject.update_count + 1

            # 申請書履歴オブジェクトを更新します。
            self.__add_history(session, applicationObject, activityObject, None)

            session.flush()

            activityObjectDao = ActivityObjectDao()
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            # 同一ルートタイプ、同一ルート番号の承認者が複数いた場合、確認に携わらなかった承認者を削除します。
            for activityObject in activityObjects:
                if activityObject.route_type == route_type and activityObject.route_number == route_number:
                    if activityObject.activity_status != ActivityStatus.AUTHORIZER_CONFIRMATION:
                        activityObjectDao.delete(session, activityObject.id)

            session.flush()

            # 次の承認者を[到着]に変更します。
            activityObjects = activityObjectDao.find_by_company_code_application_number(session, company_code, application_number)
            if activityObjects is None:
                raise LaubeException('nothing activityObjects.')

            w_route_type = None
            w_route_number = None
            for activityObject in activityObjects:
                if activityObject.route_type == route_type and activityObject.route_number == route_number:  # 自分自身を読み飛ばします。
                    pass
                else:
                    if activityObject.route_type == w_route_type and activityObject.route_number == w_route_number:
                        activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                        activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                    else:
                        if w_route_type is not None and w_route_number is not None:
                            break

                        if activityObject.activity_status == ActivityStatus.AUTHORIZER_UNTREATED and activityObject.function == ApprovalFunction.FUNCTION_CONFIRMATION:  # [未処理]且つ[確認]の場合のみ更新
                            activityObject.activity_status = ActivityStatus.ARRIVAL  # [到着]
                            activityObject.reaching_date = dt.strftime('%Y/%m/%d %H:%M:%S')  # 到着日
                            w_route_type = activityObject.route_type  # 比較条件を[到着]の申請明細に変更(並列対応)
                            w_route_number = activityObject.route_number  # 比較条件を[到着]の申請明細に変更(並列対応)
            return True

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise LaubeException(e)

        except Exception as e:
            raise LaubeException(e)

    """
    [利用場所]
    各更新処理から呼び出される事を想定しています。

    [機能]
    申請履歴を登録します。

    Args:
        session : セッション情報
        applicationObject : 申請オブジェクト
        activityObject : 申請明細オブジェクト
        applicant_status : 申請者ステータス

    Returns:
        なし

    Raises:
        例外
    """
    def __add_history(self, session, applicationObject, activityObject, applicant_status):

        try:
            if not session:
                raise LaubeException(self.E001)

            if applicationObject is None:
                raise LaubeException('required applicationObject')

            if activityObject is None:
                activityObject = ActivityObject()

            routeHistory = RouteHistory()
            routeHistory.company_code = applicationObject.target_company_code
            routeHistory.company_name = self.__get_company_name(session, applicationObject.target_company_code)
            routeHistory.application_number = applicationObject.application_number
            routeHistory.re_application_number = applicationObject.re_application_number
            routeHistory.application_form_code = applicationObject.application_form_code
            routeHistory.application_form_name, _, _ = self.__get_application_form_name(session, applicationObject.target_company_code, applicationObject.application_form_code)
            routeHistory.target_company_code = applicationObject.target_company_code
            routeHistory.target_company_name = self.__get_company_name(session, applicationObject.target_company_code)
            routeHistory.target_group_code = applicationObject.target_group_code
            routeHistory.target_group_name = self.__get_group_name(session, applicationObject.target_company_code, applicationObject.target_group_code)
            routeHistory.target_employee_code = applicationObject.target_employee_code
            routeHistory.target_employee_name = self.__get_employee_name(session, applicationObject.target_company_code, applicationObject.target_employee_code)
            routeHistory.applicant_company_code = applicationObject.applicant_company_code
            routeHistory.applicant_company_name = self.__get_company_name(session, applicationObject.applicant_company_code)
            routeHistory.applicant_group_code = applicationObject.applicant_group_code
            routeHistory.applicant_group_name = self.__get_group_name(session, applicationObject.applicant_company_code, applicationObject.applicant_group_code)
            routeHistory.applicant_employee_code = applicationObject.applicant_employee_code
            routeHistory.applicant_employee_name = self.__get_employee_name(session, applicationObject.applicant_company_code, applicationObject.applicant_employee_code)
            routeHistory.apply_date = applicationObject.apply_date
            routeHistory.application_status = applicationObject.application_status
            routeHistory.applicant_status = applicant_status
            routeHistory.route_type = activityObject.route_type
            routeHistory.route_number = activityObject.route_number
            routeHistory.approverl_company_code = activityObject.approverl_company_code
            routeHistory.approverl_company_name = self.__get_company_name(session, activityObject.approverl_company_code)
            routeHistory.approverl_group_code = activityObject.approverl_group_code
            routeHistory.approverl_group_name = self.__get_group_name(session, activityObject.approverl_company_code, activityObject.approverl_group_code)
            routeHistory.approverl_employee_code = activityObject.approverl_employee_code
            routeHistory.approverl_employee_name = self.__get_employee_name(session, activityObject.approverl_company_code, activityObject.approverl_employee_code)
            routeHistory.deputy_approverl_company_code = activityObject.deputy_approverl_company_code
            routeHistory.deputy_approverl_company_name = self.__get_company_name(session, activityObject.deputy_approverl_company_code)
            routeHistory.deputy_approverl_group_code = activityObject.deputy_approverl_group_code
            routeHistory.deputy_approverl_group_name = self.__get_group_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_group_code)
            routeHistory.deputy_approverl_employee_code = activityObject.deputy_approverl_employee_code
            routeHistory.deputy_approverl_employee_name = self.__get_employee_name(session, activityObject.deputy_approverl_company_code, activityObject.deputy_approverl_employee_code)
            routeHistory.deputy_contents = activityObject.deputy_contents
            routeHistory.function = activityObject.function
            routeHistory.reaching_date = activityObject.reaching_date
            routeHistory.process_date = activityObject.process_date
            routeHistory.activity_status = activityObject.activity_status
            routeHistory.approverl_comment = activityObject.approverl_comment
            routeHistory.create_employee_code = applicationObject.applicant_employee_code
            routeHistory.update_employee_code = applicationObject.applicant_employee_code
            routeHistory.update_count = 1

            routeHistoryDao = RouteHistoryDao()
            routeHistoryDao.add(session, routeHistory)

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    """
    [利用場所]
    Laube内なら自由に利用可能

    [機能]
    会社名を取得します。見つからない場合は(未登録)を返却します。

    Args:
        session : セッション情報
        company_code : 会社コード

    Returns:
        会社名

    Raises:
        例外
    """
    def __get_company_name(self, session, company_code):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                return '(未登録)'

            companyDao = CompanyDao()
            company = companyDao.find_ix_m_company(session, company_code)

            if company is None:
                return '(未登録)'
            else:
                return company.company_name

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    """
    [利用場所]
    Laube内なら自由に利用可能

    [機能]
    従業員名を取得します。見つからない場合は(未登録)を返却します。

    Args:
        session : セッション情報
        company_code : 会社コード
        employee_code : 従業員番号

    Returns:
        従業員名

    Raises:
        例外
    """
    def __get_employee_name(self, session, company_code, employee_code):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                return '(未登録)'

            if not employee_code:
                return '(未登録)'

            employeeDao = EmployeeDao()
            employee = employeeDao.find_ix_m_employee(session, company_code, employee_code)

            if employee is None:
                return '(未登録)'
            else:
                return employee.employee_name

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    """
    [利用場所]
    Laube内なら自由に利用可能

    [機能]
    部署名を取得します。見つからない場合は(未登録)を返却します。

    Args:
        session : セッション情報
        company_code : 会社コード
        group_code : 部署コード

    Returns:
        部署名

    Raises:
        例外
    """
    def __get_group_name(self, session, company_code, group_code):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                return '(未登録)'

            if group_code is None:
                return '(未登録)'

            groupDao = GroupDao()
            group = groupDao.find_ix_m_group(session, company_code, group_code)

            if group is None:
                return '(未登録)'
            else:
                return group.group_name

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    """
    [利用場所]
    Laube内なら自由に利用可能

    [機能]
    申請書名を取得します。見つからない場合は(未登録)を返却します。

    Args:
        session : セッション情報
        company_code : 会社コード
        application_form_code : 申請書コード

    Returns:
        申請書名

    Raises:
        例外
    """
    def __get_application_form_name(self, session, company_code, application_form_code):

        try:
            if not session:
                raise LaubeException(self.E001)

            if not company_code:
                return '(未登録)', '(未登録)'

            if application_form_code is None:
                return '(未登録)', '(未登録)'

            applicationFormDao = ApplicationFormDao()
            applicationForm = applicationFormDao.find_ix_m_application_form(session, company_code, application_form_code)

            if applicationForm is None:
                return '(未登録)', '(未登録)'
            else:
                applicationClassificationDao = ApplicationClassificationDao()
                applicationClassification = applicationClassificationDao.find_ix_m_application_classification(session, applicationForm.company_code, applicationForm.application_classification_code)

                if applicationClassification is None:
                    return applicationForm.application_form_name, '(未登録)'
                else:
                    return applicationForm.application_form_name, applicationForm.application_classification_code, applicationClassification.application_classification_name

        except LaubeException as e:
            raise e

        except ArtemisException as e:
            raise e

        except Exception as e:
            raise e

    # """
    # [利用場所]
    # Laube内なら自由に利用可能

    # [機能]
    # メール送信します。

    # Args:
    #     session : セッション情報
    #     application_number : 申請番号
    #     company_code : 会社コード
    #     employee_code : 従業員番号

    # Returns:
    #     申請書名

    # Raises:
    #     例外
    # """
    # def _send_mail_workflow(self, session, alert_junl_management_control, application_form_code, application_number, applicant_company_code, applicant_employee_code, company_code, employee_code, subject, body):

    #     try:
    #         if not session:
    #             raise LaubeException(self.E001)

    #         _mail_address = None

    #         applicationFormDao = ApplicationFormDao()
    #         applicationForm = applicationFormDao.find_ix_m_application_form(session, applicant_company_code, application_form_code)

    #         employeeDao = EmployeeDao()
    #         applicant_employee = employeeDao.find_ix_m_employee(session, applicant_company_code, applicant_employee_code)

    #         # 申請者へのメール
    #         if company_code is None and employee_code is None:

    #             employeeAlertManagementDao = EmployeeAlertManagementDao()
    #             employeeAlertManagement = employeeAlertManagementDao.find_ix_m_employee_alert_management(session, applicant_company_code, applicant_employee_code, alert_junl_management_control)

    #             # 「アラートを管理する」の場合
    #             if employeeAlertManagement is None or AlertManagementControl.MANAGED == employeeAlertManagement.alert_management_control:

    #                 # 通知方法が「MAIL」または「全て」の場合
    #                 if employeeAlertManagement is None or (AlertNotificationMethod.MAIL == employeeAlertManagement.alert_notification_method or AlertNotificationMethod.ALL == employeeAlertManagement.alert_notification_method):

    #                     _mail_address = applicant_employee.mail_address

    #                     if _mail_address is None or len(_mail_address.strip()) == 0:
    #                         pass
    #                     else:
    #                         _subject = subject
    #                         _subject = _subject.replace('{application_number}', str(application_number))

    #                         _body = body
    #                         _body = _body.replace('{application_number}', str(application_number))
    #                         _body = _body.replace('{application_form_name}', applicationForm.application_form_name)

    #                         sendGridUtility = SendGridUtility()
    #                         sendGridUtility.send_mail(_mail_address, _subject, _body)

    #         else:
    #             employeeDao = EmployeeDao()
    #             employee = employeeDao.find_availability_employee(session, company_code, employee_code, date.today())

    #             employeeAlertManagementDao = EmployeeAlertManagementDao()
    #             employeeAlertManagement = employeeAlertManagementDao.find_ix_m_employee_alert_management(session, company_code, employee_code, alert_junl_management_control)

    #             # 「アラートを管理する」の場合
    #             if employeeAlertManagement is None or AlertManagementControl.MANAGED == employeeAlertManagement.alert_management_control:

    #                 # 通知方法が「MAIL」または「全て」の場合
    #                 if employeeAlertManagement is None or (AlertNotificationMethod.MAIL == employeeAlertManagement.alert_notification_method or AlertNotificationMethod.ALL == employeeAlertManagement.alert_notification_method):

    #                     # 承認者へのメール
    #                     if employee is not None and employee.mail_address is not None:

    #                         _mail_address = employee.mail_address
    #                         _subject = subject
    #                         _subject = _subject.replace('{employee_code}', applicant_employee.employee_code)
    #                         _subject = _subject.replace('{employee_name}', applicant_employee.employee_name)
    #                         _subject = _subject.replace('{application_number}', str(application_number))

    #                         _body = body
    #                         _body = _body.replace('{employee_code}', applicant_employee.employee_code)
    #                         _body = _body.replace('{employee_name}', applicant_employee.employee_name)
    #                         _body = _body.replace('{application_number}', str(application_number))
    #                         _body = _body.replace('{application_form_name}', applicationForm.application_form_name)

    #                         sendGridUtility = SendGridUtility()
    #                         sendGridUtility.send_mail(_mail_address, _subject, _body)

    #     except LaubeException as e:
    #         raise e

    #     except ArtemisException as e:
    #         raise e

    #     except Exception as e:
    #         raise e
