import json
from typing import Optional, Any, List
from deepdiff import DeepDiff
from app.models.models import ActivityObject, ApplicationObject, ApplicationSnapshot, ApplicationComment
from app.repositories.base.application_snapshot_repository_base import ApplicationSnapshotRepositoryBase

class ApplicationSnapshotRepository(ApplicationSnapshotRepositoryBase):
    """
    ApplicationSnapshotRepositoryBase のカスタムメソッド追加用
    """

    def take_workflow_snapshot(self, db_session, application_number: int) -> dict:
        # 1. ヘッダ・明細・コメントなど全部dict化
        app_obj = db_session.query(ApplicationObject).filter_by(application_number=application_number).first()
        activities = db_session.query(ActivityObject).filter_by(application_number=application_number).all()
        comments = db_session.query(ApplicationComment).filter_by(application_number=application_number).all()

        snapshot = {
            "application": app_obj.to_dict() if app_obj else None,
            "activities": [a.to_dict() for a in activities],
            "comments": [c.to_dict() for c in comments],
        }
        return snapshot

    def get_next_version(self, db_session, application_number: int) -> int:
        last = (
            db_session.query(ApplicationSnapshot)
            .filter_by(application_number=application_number)
            .order_by(ApplicationSnapshot.version_number.desc())
            .first()
        )
        return (last.version_number + 1) if last else 1

    def save_snapshot(self, db_session, application_number: int, user_uuid: str, reason: str = "自動取得"):
        snapshot = self.take_workflow_snapshot(db_session, application_number)
        if not snapshot["application"]:
            raise ValueError("ApplicationObjectが存在しません")
        snapshot_json = json.dumps(snapshot, ensure_ascii=False, default=str)
        version = self.get_next_version(db_session, application_number)
        tenant_uuid = snapshot["application"]["tenant_uuid"]

        db_session.add(ApplicationSnapshot(
            tenant_uuid=tenant_uuid,
            application_number=application_number,
            version_number=version,
            snapshot_data=snapshot_json,
            snapshot_reason=reason,
            create_user_uuid=user_uuid,
        ))
        db_session.commit()

    def restore_workflow_snapshot(self, db_session, tenant_uuid, application_number, version_number, user_uuid):
        snapshot_row = db_session.query(ApplicationSnapshot).filter_by(
            tenant_uuid=tenant_uuid,
            application_number=application_number,
            version_number=version_number
        ).first()
        if not snapshot_row:
            raise Exception("スナップショットが見つかりません")

        data = json.loads(snapshot_row.snapshot_data)

        # 既存データ削除 or 上書き
        db_session.query(ActivityObject).filter_by(application_number=application_number).delete()
        db_session.query(ApplicationComment).filter_by(application_number=application_number).delete()
        # ...他も必要に応じて

        # ヘッダ
        if data["application"]:
            app_obj = ApplicationObject(**data["application"])
            db_session.merge(app_obj)
        # 明細
        for act in data["activities"]:
            db_session.add(ActivityObject(**act))
        # コメント
        for com in data["comments"]:
            db_session.add(ApplicationComment(**com))

        # 復元操作自体の証跡を追加
        db_session.add(ApplicationSnapshot(
            tenant_uuid=tenant_uuid,
            application_number=application_number,
            version_number=self.get_next_version(db_session, application_number),
            snapshot_data=snapshot_row.snapshot_data,
            snapshot_reason=f"ロールバック({version_number})",
            revert_to_version=version_number,
            create_user_uuid=user_uuid,
        ))
        db_session.commit()

    def compare_snapshots(self, snap1, snap2):
        """
        snap1, snap2: dict or ApplicationSnapshot
        """
        if isinstance(snap1, ApplicationSnapshot):
            snap1 = json.loads(snap1.snapshot_data)
        if isinstance(snap2, ApplicationSnapshot):
            snap2 = json.loads(snap2.snapshot_data)
        diff = DeepDiff(snap1, snap2, ignore_order=True)
        return diff

    # さらに「部分復元」や「差分適用」もこのノリで追加OK！

