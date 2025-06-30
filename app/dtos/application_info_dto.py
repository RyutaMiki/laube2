from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ApplicationInfoDto(BaseModel):
    screen_mode: Optional[str] = None  # 画面モード（新規、再申請、参照など）
    application_classification_code: Optional[str] = None  # 申請分類コード
    application_classification_name: Optional[str] = None  # 申請分類名
    application_number: int = 0  # 申請番号
    re_application_number: int = 0  # 再申請番号

    application_form_code: Optional[str] = None  # 申請書コード
    application_form_name: Optional[str] = None  # 申請書名

    target_tenant_uuid: Optional[str] = None  # 対象者のテナントUUID
    target_tenant_name: Optional[str] = None  # 対象者のテナント名
    target_group_code: Optional[str] = None  # 対象者の部署コード
    target_group_name: Optional[str] = None  # 対象者の部署名
    target_user_uuid: Optional[str] = None  # 対象者のユーザーUUID
    target_user_name: Optional[str] = None  # 対象者の氏名

    applicant_tenant_uuid: Optional[str] = None  # 申請者のテナントUUID
    applicant_tenant_name: Optional[str] = None  # 申請者のテナント名
    applicant_group_code: Optional[str] = None  # 申請者の部署コード
    applicant_group_name: Optional[str] = None  # 申請者の部署名
    applicant_user_uuid: Optional[str] = None  # 申請者のユーザーUUID
    applicant_user_name: Optional[str] = None  # 申請者の氏名

    apply_date: Optional[datetime] = None  # 申請日
    application_status: Optional[str] = None  # 申請ステータス
    applicant_status: Optional[str] = None  # 申請者の状態（差戻し中など）

    approverl_list: List[dict] = []  # 承認ルート情報（ApproverlInfoDtoなど）
    route_history_list: List[dict] = []  # 承認履歴情報

    def as_dict(self) -> dict:
        """Dict形式で取得（Pydantic v2対応）"""
        return self.model_dump()

    def to_json(self) -> str:
        """JSON文字列として取得（Pydantic v2対応）"""
        return self.model_dump_json(ensure_ascii=False)

    def __repr__(self) -> str:
        """簡易表示（ログなど用）"""
        return (
            f"<ApplicationInfoDto app_no={self.application_number}, "
            f"form={self.application_form_code}, target={self.target_user_uuid}>"
        )
