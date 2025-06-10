import json
from typing import Optional, Any, List
from deepdiff import DeepDiff
from app.models.models import ActivityObject, ApplicationObject, ApplicationSnapshot, ApplicationComment
from app.repositories.base.application_snapshot_repository_base import ApplicationSnapshotRepositoryBase

class ApplicationSnapshotRepository(ApplicationSnapshotRepositoryBase):
    """
    ApplicationSnapshotRepositoryBase のカスタムメソッド追加用クラス。
    申請に関するスナップショットの保存・復元・比較・差分適用などを提供する。
    """

    def take_workflow_snapshot(self, db_session, application_number: int) -> dict:
        """
        現在の申請状態（ヘッダ・アクティビティ・コメント）を辞書形式で取得する。

        :param db_session: データベースセッション
        :param application_number: 対象の申請番号
        :return: スナップショット辞書
        """
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
        """
        指定された申請の次のバージョン番号を取得する。

        :param db_session: データベースセッション
        :param application_number: 申請番号
        :return: 次のバージョン番号（int）
        """
        last = (
            db_session.query(ApplicationSnapshot)
            .filter_by(application_number=application_number)
            .order_by(ApplicationSnapshot.version_number.desc())
            .first()
        )
        return (last.version_number + 1) if last else 1

    def save_snapshot(self, db_session, application_number: int, user_uuid: str, reason: str = "自動取得"):
        """
        現在の申請状態をスナップショットとして保存する。

        :param db_session: データベースセッション
        :param application_number: 申請番号
        :param user_uuid: 操作ユーザーUUID
        :param reason: スナップショット保存理由（デフォルト: "自動取得"）
        :raises ValueError: ApplicationObjectが存在しない場合
        """
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
        """
        指定したスナップショットバージョンへ完全復元を行う。

        :param db_session: データベースセッション
        :param tenant_uuid: テナントUUID
        :param application_number: 申請番号
        :param version_number: 復元対象バージョン番号
        :param user_uuid: 復元操作を行うユーザーUUID
        :raises Exception: スナップショットが存在しない場合
        """
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
        2つのスナップショットの差分を比較する。

        :param snap1: dict または ApplicationSnapshot
        :param snap2: dict または ApplicationSnapshot
        :return: DeepDiff オブジェクト
        """
        if isinstance(snap1, ApplicationSnapshot):
            snap1 = json.loads(snap1.snapshot_data)
        if isinstance(snap2, ApplicationSnapshot):
            snap2 = json.loads(snap2.snapshot_data)
        diff = DeepDiff(snap1, snap2, ignore_order=True)
        return diff

    def partial_restore(self, db_session, tenant_uuid, application_number, version_number, user_uuid, restore_targets=None):
        """
        指定項目（例: 'activities', 'comments'）のみを復元する部分復元を行う。

        :param db_session: データベースセッション
        :param tenant_uuid: テナントUUID
        :param application_number: 申請番号
        :param version_number: 対象スナップショットバージョン
        :param user_uuid: 操作ユーザーUUID
        :param restore_targets: 復元対象のキー名リスト（Noneの場合は全復元）
        :raises Exception: スナップショットが見つからない場合
        """
        snapshot_row = db_session.query(ApplicationSnapshot).filter_by(
            tenant_uuid=tenant_uuid,
            application_number=application_number,
            version_number=version_number
        ).first()
        if not snapshot_row:
            raise Exception("スナップショットが見つかりません")
        data = json.loads(snapshot_row.snapshot_data)

        if not restore_targets or 'application' in restore_targets:
            # ApplicationObject（ヘッダ）復元
            if data.get("application"):
                db_session.query(ApplicationObject).filter_by(application_number=application_number).delete()
                db_session.add(ApplicationObject(**data["application"]))
        if not restore_targets or 'activities' in restore_targets:
            db_session.query(ActivityObject).filter_by(application_number=application_number).delete()
            for act in data.get("activities", []):
                db_session.add(ActivityObject(**act))
        if not restore_targets or 'comments' in restore_targets:
            db_session.query(ApplicationComment).filter_by(application_number=application_number).delete()
            for com in data.get("comments", []):
                db_session.add(ApplicationComment(**com))
        # 他テーブルも同様に追加可

        db_session.add(ApplicationSnapshot(
            tenant_uuid=tenant_uuid,
            application_number=application_number,
            version_number=self.get_next_version(db_session, application_number),
            snapshot_data=snapshot_row.snapshot_data,
            snapshot_reason=f"部分復元({restore_targets}) from version {version_number}",
            revert_to_version=version_number,
            create_user_uuid=user_uuid,
        ))
        db_session.commit()

    def create_patch(self, snapshot1_dict, snapshot2_dict):
        """
        2つのスナップショット辞書から差分（パッチ）を作成する。

        :param snapshot1_dict: 比較元スナップショット（辞書）
        :param snapshot2_dict: 比較先スナップショット（辞書）
        :return: DeepDiff の差分データ
        """
        diff = DeepDiff(snapshot1_dict, snapshot2_dict, ignore_order=True)
        return diff  # そのまま“パッチ”として扱う

    def apply_patch_to_activities(self, db_session, application_number, diff):
        """
        差分データから activities 部分の変更をDBに適用する（現状は値変更のみ対応）。

        :param db_session: データベースセッション
        :param application_number: 対象の申請番号
        :param diff: DeepDiff による差分結果（values_changedのみ処理）
        """
        if "values_changed" in diff:
            for k, v in diff["values_changed"].items():
                # 例: k = "root['activities'][2]['activity_status']"
                path = k.split('[')
                if "'activities'" in path[1]:
                    idx = int(path[2].replace("']", ""))
                    field = path[3].replace("']", "").replace("['", "")
                    new_value = v['new_value']
                    # DBから該当Activity取得
                    acts = db_session.query(ActivityObject).filter_by(application_number=application_number).all()
                    if 0 <= idx < len(acts):
                        setattr(acts[idx], field, new_value)
            db_session.commit()
