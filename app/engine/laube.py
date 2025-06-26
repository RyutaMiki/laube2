from datetime import date, datetime
from functools import wraps
from app.database.connection import get_db
from sqlalchemy.orm import Session
from app.models.specifiedValue import ActivityStatus, ApprovalFunction, AutoApproverlFlag, RouteFlag, RouteType
from app.repositories.boss_repository import BossRepository
from app.repositories.application_form_repository import ApplicationFormRepository
from app.repositories.application_form_route_repository import ApplicationFormRouteRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.employee_group_repository import EmployeeGroupRepository
from app.repositories.individual_activity_repository import IndividualActivityRepository
from app.repositories.role_repository import RoleRepository
from app.common.utility import Utility
from app.common.error_message_loader import ErrorMessageLoader
from app.exception.laubeException import LaubeException
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session


######################################################################
# Copyright 2016–2025 Ryuta Miki. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################


class Laube():

    def __init__(self):
        """
        LaubeService の初期化処理。
        必要なリポジトリおよびエラーメッセージローダーを生成する。
        """
        self.error_loader = ErrorMessageLoader()
        self.boss_repository = BossRepository()
        self.application_form_repository = ApplicationFormRepository()
        self.application_form_route_repository = ApplicationFormRouteRepository()
        self.employee_repository = EmployeeRepository()
        self.employee_group_repository = EmployeeGroupRepository()
        self.individual_activity_repository = IndividualActivityRepository()
        self.role_repository = RoleRepository()

    @staticmethod
    def health_check(f):
        """
        エンジンのメンテナンス状態を確認するデコレータ。
        セッションの第1引数（通常はDBセッション）を渡してメンテナンス判定を行い、
        稼働不可状態であれば LaubeException をスローする。

        Args:
            f (Callable): 対象メソッド

        Returns:
            Callable: ラップされたメソッド（メンテナンスチェック付き）
        """
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if self.engineUtility.is_mentenance(args[0], 'Laube'):
                raise LaubeException(self.W001)
            return f(self, *args, **kwargs)
        return wrapper

    def is_display_boss_field(
        self,
        db_session: Session,
        tenant_uuid: str,
        target_group_code: str,
        target_user_uuid: str,
        application_form_code: str
    ) -> bool:
        """
        申請フォームに「上司入力欄」を表示する必要があるかを判定する。

        判定基準：
        - フォームのルート種別（route_flag）に応じて分岐
        - 個別ルートが設定されているか
        - 上司マスタが存在するか など

        パラメータ:
        ----------
        db_session : Session
            データベースセッション
        tenant_uuid : str
            テナントUUID（マルチテナント対応）
        target_group_code : str
            対象のグループコード（例：部署）
        target_user_uuid : str
            対象のユーザーUUID
        application_form_code : str
            申請フォームのコード

        戻り値:
        -------
        bool
            True: 上司入力欄を表示する
            False: 表示しない

        例外:
        -------
        LaubeException
            パラメータ不足または内部処理エラー
        """
        try:
            # 各引数のバリデーション
            if not db_session:
                msg = self.error_loader.get_message("Laube-E001")
                raise LaubeException("Laube-E001", msg)

            if not tenant_uuid:
                msg = self.error_loader.get_message("Laube-E002")
                raise LaubeException("Laube-E002", msg)

            if not target_group_code:
                msg = self.error_loader.get_message("Laube-E003")
                raise LaubeException("Laube-E003", msg)

            if not target_user_uuid:
                msg = self.error_loader.get_message("Laube-E004")
                raise LaubeException("Laube-E004", msg)

            if not application_form_code:
                msg = self.error_loader.get_message("Laube-E005")
                raise LaubeException("Laube-E005", msg)

            # 申請フォームの取得（存在チェック）
            application_form = self.application_form_repository.get_by_code(
                db_session, tenant_uuid, application_form_code
            )
            if application_form is None:
                raise LaubeException(self.E006)

            # ルート種別が「直接部門なし」の場合 → 上司入力欄は不要
            if RouteFlag.NO_INDIVIDUAL_ROUTE == application_form.route_flag:
                return False

            # ルート種別が「直接部門有り」の場合
            elif RouteFlag.INDIVIDUAL_ROUTE == application_form.route_flag:
                # 指定されたグループの直接部門ルートを取得
                application_form_route = self.application_form_route_repository.get_by_code_and_group(
                    db_session, tenant_uuid, application_form_code, target_group_code
                )
                # グループ未指定（共通）ルートも探す
                if not application_form_route:
                    application_form_route = self.application_form_route_repository.get_by_code_and_group(
                        db_session, tenant_uuid, application_form_code, None
                    )
                # 直接部門ルートコードが設定されている場合 → 上司入力欄は不要
                if application_form_route and application_form_route.individual_route_code and application_form_route.individual_route_code.strip():
                    return False
                # 直接部門ルートが未設定なら → 上司欄の可能性あり（下に続く）

            # ルート種別が「上司ルート」の場合
            elif RouteFlag.BOSS_ROUTE == application_form.route_flag:

                # 優先度順に上司マスタを検索（以下、OR条件）
                boss = (
                    self.boss_repository.get_by_all_keys(db_session, tenant_uuid, target_group_code, target_user_uuid, application_form_code)
                    or self.boss_repository.get_by_group_null(db_session, tenant_uuid, target_user_uuid, application_form_code)
                    or self.boss_repository.get_by_form_null(db_session, tenant_uuid, target_group_code, target_user_uuid)
                    or self.boss_repository.get_by_group_and_form_null(db_session, tenant_uuid, target_user_uuid)
                )

                # 上司情報が1件も見つからない → 手入力が必要 → 入力欄を表示
                if boss is None:
                    return True

            # どのルート種別にも当てはまらない（異常値）
            else:
                raise LaubeException(self.E007)

            # デフォルトは「表示しない」
            return False

        except LaubeException:
            # 自前のバリデーションエラーなどはそのまま投げ直す
            raise
        except Exception as e:
            # その他想定外のエラーもラップして投げる
            raise LaubeException(e)

    def get_individual_approverl_list(self, db_session, tenant_uuid, target_tenant_uuid, individual_route_code, application_form):
        """
        個別ルートに基づく承認者リストを取得します。

        [利用想定]
            - get_application_info() 内での呼び出しを前提としています。
            - individual_route_code に設定された個別アクティビティを基に承認ルートを生成します。

        [機能]
            - 個別アクティビティを取得し、承認者情報（従業員またはロール）に変換。
            - approverl_role_code が空の場合は、従業員情報と所属部署情報を検証。
            - ロール名は別途 Role マスタから取得。
            - 自動承認フラグ（application_form.auto_approverl_flag）が有効な場合は、ルート重複によって自動承認フラグを設定。

        Args:
            db_session (Session): SQLAlchemyのDBセッション
            tenant_uuid (str): 呼び出し元テナントのUUID（共通情報・ログ用など）
            target_tenant_uuid (str): 対象となる個別ルートの所属テナントUUID（データ取得対象）
            individual_route_code (str): 個別ルートコード（個別アクティビティ紐付けキー）
            application_form (ApplicationForm): 申請書マスタ情報（自動承認フラグなど参照）

        Returns:
            List[ApproverlDataInfoDto]: 個別アクティビティに基づく承認者DTOリスト

        Raises:
            LaubeException:
                - Laube-E001: DBセッション未指定
                - Laube-E002: tenant_uuid 未指定
                - Laube-E006: application_form が None
                - Laube-E012: 承認者の社員または部署情報が取得できない
                - Laube-E013: ロール情報が取得できない
                - UNEXPECTED: 上記以外の想定外エラー
        """
        try:
            # 各引数のバリデーション
            if not db_session:
                msg = self.error_loader.get_message("Laube-E001")
                raise LaubeException("Laube-E001", msg)

            if not tenant_uuid:
                msg = self.error_loader.get_message("Laube-E002")
                raise LaubeException("Laube-E002", msg)

            if not individual_route_code:
                return []

            if application_form is None:
                msg = self.error_loader.get_message("Laube-E006")
                raise LaubeException("Laube-E006", msg)

            utility = Utility()
            system_date = utility.convert_datetime_2_date(datetime.now())

            activities = self.individual_activity_repository.find_by_tenant_and_route(db_session, tenant_uuid, target_tenant_uuid, individual_route_code)

            if not activities:
                return []

            approver_list = []
            route_employee_codes = set()

            for activity in activities:
                # approverl_role_code が設定されていない＝個人指定
                if not activity.approverl_role_code or not activity.approverl_role_code.strip():
                    employee = self.employee_repository.find_active_employee(
                        db_session,
                        tenant_uuid,
                        activity.approverl_company_code,
                        activity.approverl_employee_code
                    )

                    if not employee:
                        msg = self.error_loader.get_message("Laube-E012")
                        raise LaubeException("Laube-E012", msg)

                    if employee.logical_deletion or (employee.retirement_date and employee.retirement_date < system_date):
                        continue

                    emp_group = self.employee_group_repository.find_by_keys(
                        db_session, tenant_uuid, activity.approverl_company_code,
                        activity.approverl_employee_code, activity.approverl_group_code
                    )

                    if not emp_group or (emp_group.term_to and emp_group.term_to < system_date):
                        msg = self.error_loader.get_message("Laube-E012")
                        raise LaubeException("Laube-E012", msg)

                dto = ApproverlDataInfoDto()
                dto.tenant_uuid = tenant_uuid
                dto.company_code = activity.company_code
                dto.company_name = self.__get_company_name(db_session, activity.company_code)
                dto.route_type = RouteType.INDIVIDUAL_ROUTE
                dto.route_number = activity.activity_code
                dto.approverl_company_code = activity.approverl_company_code
                dto.approverl_company_name = self.__get_company_name(db_session, activity.approverl_company_code)
                dto.approverl_role_code = activity.approverl_role_code
                dto.approverl_group_code = activity.approverl_group_code
                dto.approverl_group_name = self.__get_group_name(db_session, activity.approverl_company_code, activity.approverl_group_code)
                dto.approverl_employee_code = activity.approverl_employee_code
                dto.approverl_employee_name = self.__get_employee_name(db_session, activity.approverl_company_code, activity.approverl_employee_code)
                dto.activity_status = ActivityStatus.AUTHORIZER_UNTREATED
                dto.approval_function = activity.function

                # ロール名取得（ある場合）
                if activity.approverl_role_code:
                    role = self.role_repository.find_by_code(
                        db_session, tenant_uuid, activity.approverl_company_code, activity.approverl_role_code
                    )
                    if not role:
                        msg = self.error_loader.get_message("Laube-E013", activity.approverl_role_code)
                        raise LaubeException("Laube-E013", msg)
                    dto.approverl_role_name = role.role_name

                # 自動承認フラグ判定（重複防止）
                if AutoApproverlFlag.AUTOMATIC_APPROVAL == application_form.auto_approverl_flag:
                    if activity.approverl_employee_code in route_employee_codes:
                        dto.approval_function = ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL
                    route_employee_codes.add(activity.approverl_employee_code)

                approver_list.append(dto)

            return approver_list

        except LaubeException as e:
            raise e
        except Exception as e:
            raise LaubeException("UNEXPECTED", str(e))
