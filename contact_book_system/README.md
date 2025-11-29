# 連絡帳管理システム (Contact Book System)

公立中学校向けのデジタル連絡帳管理システムです。保護者、教師、生徒、養護教諭間のコミュニケーションを円滑にし、業務効率化を支援します。

## 🚀 主な機能

*   **認証・権限管理**: JWTを使用したセキュアな認証と、ロールベース（管理者、教師、生徒、養護教諭）のアクセス制御。
*   **デジタル連絡帳**: 日々の連絡事項、健康状態、学習記録のデジタル化。
*   **リアルタイムチャット**: WebSocketを使用したリアルタイムなメッセージ交換（クラス連絡、職員間連絡など）。
*   **アカウント管理**: 教職員や生徒のアカウント作成・編集・削除。
*   **アーカイブ機能**: 卒業生データの自動アーカイブと保存期間管理。

## 🛠 技術スタック

| カテゴリ | 技術 |
| :--- | :--- |
| **フロントエンド** | Vue.js 3, Bootstrap 5, WebSocket API |
| **バックエンド** | Python 3.12, FastAPI, SQLAlchemy, Pydantic |
| **データベース** | MySQL 8.4 (LTS) |
| **インフラ** | Docker, Docker Compose |

## 📂 ディレクトリ構成

```
.
├── backend/                # FastAPI バックエンド
│   ├── app/                # アプリケーションコード
│   ├── scripts/            # ユーティリティスクリプト (DB初期化, データ投入など)
│   └── Dockerfile          # バックエンド用 Dockerfile
├── frontend/               # Vue.js フロントエンド
│   └── Dockerfile          # フロントエンド用 Dockerfile
├── docker-compose.yml      # コンテナ構成定義
├── setup_dev.sh            # 開発用セットアップスクリプト
├── setup_prod.sh           # 本番用セットアップスクリプト
├── init.sql                # データベース初期化SQL (イベント定義など)
└── .env                    # 環境変数設定ファイル (git管理外)
```

## ⚙️ セットアップ & 起動

### 前提条件

*   Docker がインストールされていること
    *   **推奨バージョン**: Docker Desktop 4.x以上 / Docker Engine 24.x以上 (Docker Compose v2)
    *   **古いバージョンを使用している場合**: `docker compose` コマンドが使用できないことがあります。その場合は `docker-compose` (ハイフンあり) を代わりに使用してください。
        *   例: `docker-compose up -d`
        *   `docker-compose.yml` の `version` 属性に関する警告が表示されることがありますが、動作には影響ありません。

### 1. 初回セットアップ

用途に合わせて以下のスクリプトを実行してください。

**開発環境用 (サンプルデータあり)**:
```bash
./tools/setup_dev.sh
```
※ コンテナ起動、DB初期化、全アカウント作成、サンプルデータ投入が行われます。

**本番環境用 (最小構成)**:
```bash
./tools/setup_prod.sh
```
※ コンテナ起動、DB初期化、管理者アカウントのみ作成が行われます。

### 2. 通常起動

セットアップ完了後は、以下のコマンドで起動できます。

```bash
docker compose up -d
```

### 3. アクセス

*   **フロントエンド**: http://localhost:8080
*   **バックエンドAPI**: http://localhost:8000
*   **APIドキュメント (Swagger UI)**: http://localhost:8000/docs

## 🔐 ログイン情報（開発用初期データ）

開発環境用に以下の初期アカウントが作成されます。

| ロール | ID | ユーザー名 | パスワード | 権限概要 |
| :--- | :--- | :--- | :--- | :--- |
| **管理者** | 1 | システム管理者 | `admin123` | 全機能へのアクセス、アカウント管理 |
| **養護教諭** | 2 | 田中 花子 | `nurse123` | 生徒の健康状態確認、専用チャット |
| **教師** | 3 | 佐藤 太郎 | `teacher123` | クラス管理、連絡帳確認、チャット |
| **生徒** | 6 | 青木 一郎 | `student123` | 連絡帳記入、クラスチャット閲覧 |

## 🔧 管理・運用

### パスワードの一括リセット

全アカウントのパスワードを初期値にリセットする場合：

```bash
docker compose exec backend python scripts/update_passwords.py
```

### 環境変数 (.env)

`docker-compose.yml` は `.env` ファイルから環境変数を読み込みます。セキュリティのため、本番環境では適切な値を設定してください。

```ini
MYSQL_ROOT_PASSWORD=rootpass
MYSQL_DATABASE=renrakucho_db
MYSQL_USER=root
MYSQL_PASSWORD=rootpass
DATABASE_HOST=mysql
DATABASE_PORT=3306
```

## 🧪 テストの実行

### バックエンド

```bash
./tools/test_backend.sh
```

### フロントエンド

```bash
./tools/test_frontend.sh
```
