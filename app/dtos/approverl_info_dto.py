from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ApproverlInfoDto(BaseModel):
    tenant_uuid: Optional[str] = None  # 申請書の所属テナントUUID
    tenant_name: Optional[str] = None  # テナント名
    application_number: int = 0  # 申請番号

    target_tenant_uuid: Optional[str] = None  # 対象者のテナントUUID
    target_tenant_name: Optional[str] = None  # 対象者のテナント名
    target_group_code: Optional[str] = None  # 対象者の所属部署コード
    target_group_name: Optional[str] = None  # 対象者の所属部署名
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
    applicant_status: Optional[str] = None  # 申請者ステータス（差戻し中など）

    route_type: int = 0  # 承認ルート種別（個別/共通/上司など）
    route_number: int = 0  # 承認ルート番号（ステップ順序）

    approverl_tenant_uuid: Optional[str] = None  # 承認者のテナントUUID
    approverl_tenant_name: Optional[str] = None  # 承認者のテナント名
    approverl_role_code: Optional[str] = None  # 承認者のロールコード（ロール承認時）
    approverl_role_name: Optional[str] = None  # 承認者のロール名
    approverl_group_code: Optional[str] = None  # 承認者の部署コード
    approverl_group_name: Optional[str] = None  # 承認者の部署名
    approverl_user_uuid: Optional[str] = None  # 承認者のユーザーUUID（個人承認時）
    approverl_user_name: Optional[str] = None  # 承認者の氏名

    deputy_approverl_tenant_uuid: Optional[str] = None  # 代理承認者のテナントUUID
    deputy_approverl_tenant_name: Optional[str] = None  # 代理承認者のテナント名
    deputy_approverl_group_code: Optional[str] = None  # 代理承認者の部署コード
    deputy_approverl_group_name: Optional[str] = None  # 代理承認者の部署名
    deputy_approverl_user_uuid: Optional[str] = None  # 代理承認者のユーザーUUID
    deputy_approverl_user_name: Optional[str] = None  # 代理承認者の氏名
    deputy_contents: Optional[str] = None  # 代理承認の理由・コメント

    approval_function: Optional[str] = None  # 承認画面での機能種別（通常承認、代理承認など）
    reaching_date: Optional[datetime] = None  # 到達日（承認ステップに到達した日）
    process_date: Optional[datetime] = None  # 処理日（実際に承認された日）
    activity_status: Optional[str] = None  # 承認ステータス（未処理、承認済など）
    approverl_comment: Optional[str] = None  # 承認者のコメント

    def as_dict(self) -> dict:
        """Dict形式で取得（Pydantic v2対応）"""
        return self.model_dump()

    def to_json(self) -> str:
        """JSON形式文字列で出力（Pydantic v2対応）"""
        return self.model_dump_json(ensure_ascii=False)

    def __repr__(self) -> str:
        """簡易表示（ログ・デバッグ用）"""
        return (
            f"<ApproverlInfoDto user={self.approverl_user_uuid or self.approverl_role_code}, "
            f"status={self.activity_status}, route={self.route_type}-{self.route_number}>"
        )
