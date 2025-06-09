from datetime import date, datetime
from functools import wraps
from app.database.connection import get_db
from sqlalchemy.orm import Session
from app.models.specifiedValue import RouteFlag
from app.repositories.boss_repository import BossRepository
from app.exception.laubeException import LaubeException

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
        [利用場所]
        申請画面のInitAPIにて呼び出されることを想定しています。

        [機能]
        上司マスタの登録ができていない従業員が新規申請を行う際、
        「上司入力欄」を表示するべきかどうかを判定します。

        Args:
            db_session            : DBセッション（Repository経由で使用）
            tenant_uuid           : テナントUUID（会社単位）
            target_group_code     : 対象者の部署コード
            target_user_uuid      : 対象者のユーザーUUID
            application_form_code : 対象の申請書コード

        Returns:
            True  -> 上司入力欄を表示
            False -> 上司入力欄は不要

        Raises:
            LaubeException
        """
        try:
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

            # 申請書マスタ取得
            application_form = self.application_form_repository.get_by_code(
                db_session, tenant_uuid, application_form_code
            )
            if application_form is None:
                raise LaubeException(self.E006)

            # 直接部門ルート「なし」→ 上司入力欄は不要
            if application_form.route_flag == RouteFlag.NO_INDIVIDUAL_ROUTE:
                return False

            # 個別ルート判定
            elif application_form.route_flag == RouteFlag.INDIVIDUAL_ROUTE:
                route = self.application_form_route_repository.get_by_code_and_group(
                    db_session, tenant_uuid, application_form_code, target_group_code
                )
                if not route:
                    route = self.application_form_route_repository.get_by_code_and_group(
                        db_session, tenant_uuid, application_form_code, None
                    )
                if route and route.individual_route_code and route.individual_route_code.strip():
                    return False  # ルートが設定されていれば上司入力欄は不要

            # 上司ルート
            elif application_form.route_flag == RouteFlag.BOSS_ROUTE:
                repo = self.boss_repository
                boss = (
                    repo.get_by_all_keys(db_session, tenant_uuid, target_group_code, target_user_uuid, application_form_code)
                    or repo.get_by_group_null(db_session, tenant_uuid, target_user_uuid, application_form_code)
                    or repo.get_by_form_null(db_session, tenant_uuid, target_group_code, target_user_uuid)
                    or repo.get_by_group_and_form_null(db_session, tenant_uuid, target_user_uuid)
                )
                if boss is None:
                    return True  # 上司マスタが見つからない → 入力欄を表示

            else:
                raise LaubeException(self.E007)

            return False

        except LaubeException:
            raise
        except Exception as e:
            raise LaubeException(e)
