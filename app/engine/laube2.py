from datetime import date, datetime
from functools import wraps
from app.database.connection import get_db
from sqlalchemy.orm import Session
from app.models.specifiedValue import RouteFlag
from app.repositories.boss_repository import BossRepository
from app.exception.laubeException import LaubeException
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session


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


class Laube2():

    def __init__(self):
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

        self.boss_repository = BossRepository()

    def health_check(f):
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
                raise LaubeException(self.E001)
            if not tenant_uuid:
                raise LaubeException(self.E002)
            if not target_group_code:
                raise LaubeException(self.E003)
            if not target_user_uuid:
                raise LaubeException(self.E004)
            if not application_form_code:
                raise LaubeException(self.E005)

            # 申請フォームの取得（存在チェック）
            application_form = self.application_form_repository.get_by_code(
                db_session, tenant_uuid, application_form_code
            )
            if application_form is None:
                raise LaubeException(self.E006)

            # ルート種別が「個別ルートなし」の場合 → 上司入力欄は不要
            if application_form.route_flag == RouteFlag.NO_INDIVIDUAL_ROUTE:
                return False

            # ルート種別が「個別ルートあり」の場合
            elif application_form.route_flag == RouteFlag.INDIVIDUAL_ROUTE:
                # 指定されたグループの個別ルートを取得
                route = self.application_form_route_repository.get_by_code_and_group(
                    db_session, tenant_uuid, application_form_code, target_group_code
                )
                # グループ未指定（共通）ルートも探す
                if not route:
                    route = self.application_form_route_repository.get_by_code_and_group(
                        db_session, tenant_uuid, application_form_code, None
                    )
                # 個別ルートコードが設定されている場合 → 上司入力欄は不要
                if route and route.individual_route_code and route.individual_route_code.strip():
                    return False
                # 個別ルートが未設定なら → 上司欄の可能性あり（下に続く）

            # ルート種別が「上司ルート」の場合
            elif application_form.route_flag == RouteFlag.BOSS_ROUTE:
                repo = self.boss_repository

                # 優先度順に上司マスタを検索（以下、OR条件）
                boss = (
                    repo.get_by_all_keys(db_session, tenant_uuid, target_group_code, target_user_uuid, application_form_code)
                    or repo.get_by_group_null(db_session, tenant_uuid, target_user_uuid, application_form_code)
                    or repo.get_by_form_null(db_session, tenant_uuid, target_group_code, target_user_uuid)
                    or repo.get_by_group_and_form_null(db_session, tenant_uuid, target_user_uuid)
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

    def get_application_info(
        self,
        db_session: Session,
        tenant_uuid: str,
        application_form_code: str,
        target_group_code: str,
        target_user_uuid: str,
        boss_group_code: Optional[str],
        boss_user_uuid: Optional[str],
        applicant_group_code: str,
        applicant_user_uuid: str
    ) -> ApplicationInfoDto:
        """
        申請モード1における申請情報を構築する（対象者・申請者・承認ルート）

        Returns:
            ApplicationInfoDto: UIに渡す申請用DTO
        Raises:
            LaubeException: 各種マスタが存在しない場合など
        """
        if not db_session:
            raise LaubeException(self.E001)
        if not tenant_uuid:
            raise LaubeException(self.E002)
        if not target_group_code:
            raise LaubeException(self.E003)
        if not target_user_uuid:
            raise LaubeException(self.E004)
        if not application_form_code:
            raise LaubeException(self.E005)
        if not applicant_group_code:
            raise LaubeException(self.E009)
        if not applicant_user_uuid:
            raise LaubeException(self.E010)

        system_date = datetime.now()
        dto = ApplicationInfoDto()
        dto.screen_mode = ScreenMode.APPLY_MODE_1
        dto.application_form_code = application_form_code

        # 各種マスタ取得
        form = self.application_form_repository.get_by_code(db_session, tenant_uuid, application_form_code)
        if not form:
            raise LaubeException(self.E006)

        classification = self.application_classification_repository.get_by_code(
            db_session, tenant_uuid, form.application_classification_code
        )
        if not classification:
            raise LaubeException(self.E011)

        dto.application_form_name = form.application_form_name
        dto.application_classification_code = classification.application_classification_code
        dto.application_classification_name = classification.application_classification_name

        # 対象者
        dto.target_group_code = target_group_code
        dto.target_group_name = self.group_repository.get_name(db_session, tenant_uuid, target_group_code)
        dto.target_user_uuid = target_user_uuid
        dto.target_user_name = self.employee_repository.get_name(db_session, tenant_uuid, target_user_uuid)

        # 申請者
        dto.applicant_group_code = applicant_group_code
        dto.applicant_group_name = self.group_repository.get_name(db_session, tenant_uuid, applicant_group_code)
        dto.applicant_user_uuid = applicant_user_uuid
        dto.applicant_user_name = self.employee_repository.get_name(db_session, tenant_uuid, applicant_user_uuid)

        # 申請書ルート情報取得（個別/共通）
        form_route = self.application_form_route_repository.get_by_code_and_group(
            db_session, tenant_uuid, application_form_code, target_group_code
        ) or self.application_form_route_repository.get_by_code_and_group(
            db_session, tenant_uuid, application_form_code, None
        )

        approver_list = []

        if form.route_flag == RouteFlag.INDIVIDUAL_ROUTE:
            if form_route and form_route.individual_route_code:
                approver_list = self.__get_individual_approver_list(
                    db_session, tenant_uuid, form_route.individual_route_code, form
                )
        elif form.route_flag == RouteFlag.BOSS_ROUTE:
            approver_list = self.__get_boss_approver_list(
                db_session, tenant_uuid, target_group_code, target_user_uuid,
                application_form_code, boss_group_code, boss_user_uuid, form.job_title_code
            )
            if not approver_list:
                approver_list = self.__get_individual_approver_list(
                    db_session, tenant_uuid, classification.individual_route_code, form
                )

        # 間接ルート（共通ルート）があれば適用
        if form_route and form_route.common_route_code:
            approver_list = self.__get_common_approver_list(
                db_session, tenant_uuid, form_route.common_route_code, approver_list
            )

        # 申請者がルートに含まれる場合 → 自動承認処理
        has_applicant = any(
            a.approver_user_uuid == applicant_user_uuid and
            a.approver_group_code == applicant_group_code
            for a in approver_list
        )
        new_approver_list = []
        if form.skip_apply_employee and has_applicant:
            reached = False
            for idx, approver in enumerate(approver_list, 1):
                dto_ = ApproverDto()
                dto_.route_number = idx
                dto_.approver_user_uuid = approver.approver_user_uuid
                dto_.approver_group_code = approver.approver_group_code
                dto_.approver_group_name = self.group_repository.get_name(db_session, tenant_uuid, approver.approver_group_code)
                dto_.approver_employee_name = self.employee_repository.get_name(db_session, tenant_uuid, approver.approver_user_uuid)
                dto_.route_type = RouteType.INDIVIDUAL_ROUTE
                dto_.apply_date = None

                if approver.approver_user_uuid == applicant_user_uuid:
                    dto_.activity_status = ActivityStatus.AUTHORIZER_AUTOMATIC_APPROVAL
                    dto_.approval_function = ApprovalFunction.AUTHORIZER_AUTOMATIC_APPROVAL
                    dto_.approver_comment = "申請者本人のため自動承認"
                    dto_.reaching_date = system_date
                    dto_.process_date = system_date
                    reached = True
                else:
                    if reached:
                        dto_.activity_status = ActivityStatus.AUTHORIZER_UNTREATED
                        dto_.reaching_date = None
                        dto_.process_date = None
                    else:
                        dto_.activity_status = ActivityStatus.AUTHORIZER_AUTOMATIC_APPROVAL
                        dto_.reaching_date = system_date
                        dto_.process_date = system_date
                    dto_.approval_function = approver.approval_function

                new_approver_list.append(dto_)
            dto.approver_list = new_approver_list
        else:
            dto.approver_list = approver_list

        return dto






