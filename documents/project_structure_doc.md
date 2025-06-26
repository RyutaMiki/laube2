# プロジェクト構成説明 (Markdown)

このドキュメントは `laube2` プロジェクトのファイル/フォルダ構成とその意図を解説します。

---

##  🗂 ルートファイル

```
laube2/
├── .vscode/              # VSCodeのローカル設定
├── alembic/              # Alembicマイグレーション関連
├── app/                  # メインアプリケーションコード
├── documents/            # 資料やメモ、ギフアニメーション
├── tests/                # pytest用テストコード
├── tools/                # コード生成スクリプト
├── .env / .gitignore     # 環境変数とgit無視設定
├── requirements.txt      # 依存ライブラリ
├── pytest.ini            # pytest設定
```

---

## 📂 `app/`

**メインプロジェクトのソースコード一\u式**

### サブフォルダ構成

- `api/`：FastAPIルート用APIルーター
- `common/`：ユーティリティ系/メッセージローダー
- `config/`：YAMLスキーマ
- `constants/`：コンスタントデータ (error messages, etc.)
- `daos/`：DAO (データアクセスオブジェクト)
- `database/`：DBセッション調築/接続
- `dependencies/`：DIや認証依存モジュール
- `engine/`：コアロジックエンジン (Laube2)
- `exception/`：例外処理
- `models/`：SQLAlchemy ORMモデル & Enum
- `repositories/`：ロジックレイヤー (DAO へのブリッジ)
- `routers/`：FastAPI ルーターグループ
- `schemas/`：Pydantic schema パス (未使用?)
- `services/`：ビジネスロジック (手続ロジック)
- `templates/`：Jinja2 テンプレート用
- `utils/`：JWTトークン系 ユーティリティ

---

## 📂 `tests/`

**pytestベースのテストコード**

- `dao/`：DAO テスト (各DAOに1テスト)
- `repositories/`：リポジトリテスト
- `services/`：Serviceのロジックテスト
- `engine/`：Laube2ロジックテスト
- `db/`：DBテスト用テーブルチェック
- `conftest.py`：pytest用fixture

---

## 🔧 `tools/`

**自動生成スクリプト系**

- `generate_models.py`：YAML → ORMモデル
- `generate_stub_repository.py` など：DAO/リポジトリー/サービススタブ生成
- `generate_dao_pytest.py`：DAO用pytestテスト生成

---

## 📄 `documents/`

**メモやアニメーション資料**

- `memo.txt`：手続記録
- `gif/`：workflowアニメーション画像

---

## 📁 `alembic/`

**DBマイグレーション関連スクリプト**

- `env.py`：Alembic設定
- `versions/`：マイグレーションSQL

---

## 📓 ルートディレクトリ配置

- `main.py`：FastAPI エントリーポイント
- `__init__.py`：パッケージ化

---

必要であれば「テーブル構成のER」や「継承チェーン」の説明も追加できます。
