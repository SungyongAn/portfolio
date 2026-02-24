# 連絡帳管理システム

学校向け連絡帳のデジタル管理システム。生徒の日々の記録を効率的に管理し、教師との円滑なコミュニケーションを実現します。

## 技術スタック

### Backend
- **Framework**: FastAPI 0.115.5
- **Database**: MySQL 8.0 (Docker)
- **ORM**: SQLAlchemy 2.0.36
- **Migration**: Alembic 1.14.0
- **Authentication**: JWT (python-jose) + Password Hashing (passlib + argon2)
  - アクセストークンはメモリで管理
  - リフレッシュトークンは HttpOnly Cookie で管理（XSS 攻撃に対する安全性向上）
  - bcrypt の Python 3.12 互換問題を回避するため argon2 を採用
- **Python**: 3.11 / 3.12（Docker開発環境）
- **Package Manager**: uv

### Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite 5
- **UI**: Bootstrap 5 + Bootstrap Icons
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Development**: Windows (VSCode)
- **Hot Reload**: Docker volume mount + Uvicorn / Vite dev server

## プロジェクト構造
```
re_contact_book_system/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemyモデル
│   │   ├── schemas/         # Pydanticスキーマ
│   │   ├── routers/         # APIエンドポイント
│   │   ├── services/        # ビジネスロジック
│   │   ├── db.py            # DB接続設定
│   │   ├── dependencies/    # 認証・依存性注入
│   │   │   └── auth.py
│   │   └── main.py          # FastAPIアプリ
│   ├── alembic/             # マイグレーション
│   ├── scripts/             # 補助スクリプト
│   ├── requirements.txt     # Python依存関係
│   └── .env                 # 環境変数
├── frontend/
│   ├── src/
│   │   ├── views/           # ページコンポーネント
│   │   ├── components/      # 再利用コンポーネント
│   │   ├── stores/          # Pinia状態管理
│   │   ├── services/        # API通信
│   │   ├── router/          # ルーティング
│   │   └── main.js          # エントリーポイント
│   ├── package.json
│   └── .env                 # 環境変数
├── docker-compose.yml       # Docker共通設定
├── docker-compose.dev.yml   # 開発環境用Docker設定
├── docker-compose.prod.yml  # 本番環境用Docker設定
├── seed.sql                 # テストデータ投入スクリプト
└── docs/
    ├── INDEX.md             # ドキュメント一覧
    ├── er_diagram.mmd       # ER図（Mermaid形式）
    ├── archive/             # 旧バージョンのドキュメント
    ├── changelog/           # コンポーネント別変更履歴
    │   ├── CHANGELOG-backend.md
    │   ├── CHANGELOG-frontend.md
    │   └── CHANGELOG-database.md
    └── design/              # 設計ドキュメント
        ├── auth-design.md
        ├── teacher-assignment-design.md
        └── login-response-design.md
```
※ 開発環境では Docker を使用しており、ローカルの仮想環境（.venv）はリポジトリには含めていません。

## セットアップ

本プロジェクトは **Docker / Docker Compose を前提とした開発環境** を採用しています。  
バックエンド（FastAPI）・フロントエンド（Vue.js）ともに Docker コンテナ上で起動し、  
ホットリロードが有効な状態で開発できます。

---

### 前提条件

以下がローカル環境にインストールされていることを確認してください。

- **Docker Desktop**：最新版
- **Node.js**：18 以上（※フロントエンドを Docker 外で作業する場合）
- **Git**

※ Python や uv をローカルにインストールする必要はありません。

---

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd re_contact_book_system
```

### 2. 環境変数ファイルの作成

#### バックエンド

```bash
cd backend
cp .env.example .env
```
.env を編集し、データベース接続情報などを環境に合わせて設定してください。

#### フロントエンド

```bash
cd frontend
cp .env.example .env
```

例：
```bash
VITE_API_URL=http://localhost:8000
```

### 3. Docker コンテナの起動（開発環境）

本プロジェクトでは、  
共通設定（`docker-compose.yml`）と  
開発環境用設定（`docker-compose.dev.yml`）を組み合わせて起動します。

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

### 補足（本番環境について）

本番環境では `docker-compose.prod.yml` を使用して起動します。
開発環境とは異なり、ホットリロードやソースコードの volume マウントは行いません。

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

起動中のコンテナを確認：

```bash
docker ps
```

### 4. データベースの初期化（初回のみ）

MySQLコンテナの初回起動時に、環境変数 `MYSQL_DATABASE` により
データベース `journal_system` が自動作成されます。

続いてマイグレーションを実行し、テーブルを作成します。

```bash
docker compose exec backend alembic upgrade head
```

続いて、テストデータを投入します。

```bash
docker compose exec -T db mysql -u root -proot --default-character-set=utf8mb4 journal_system < seed.sql
```

### ■ Windows環境での注意（重要）

Windows環境では、PowerShell や一部のターミナルを使用した場合、  
リダイレクト実行時の文字コード差異により **日本語データが文字化けする可能性があります。**

その場合は **コマンドプロンプト（cmd）での実行を推奨** します。

#### ✔ 推奨手順（cmd）

1. コマンドプロンプトを開く  
2. プロジェクトのルートディレクトリへ移動  
3. 以下を実行

```bash
docker compose exec -T db mysql -u root -proot --default-character-set=utf8mb4 journal_system < seed.sql
```

※ 上記コマンドでも文字化けする場合は、seed.sql の保存文字コードが UTF-8 (BOMなし) になっているか確認してください。

> **注意**: `seed.sql` は日付依存データ等を含まない開発用テストデータのみを対象としています。本番環境では `seed.sql` の実行は不要です。

### 5. 起動確認

- **バックエンド（FastAPI）**  
  http://localhost:8000  
  - Swagger UI: http://localhost:8000/docs  
  - ReDoc: http://localhost:8000/redoc  

- **フロントエンド（Vue + Vite）**  
  http://localhost:5173  

コードを編集すると、バックエンド・フロントエンドともに  
**ホットリロードにより自動で再読み込み**されます。

### 6. コンテナの停止
```bash
docker compose down
```

## スクリプト

### API 経由で日誌を作成するスクリプト
- ファイル: scripts/create_journal_via_api.py
- 目的: API を通じて日誌エントリを作成する補助スクリプト
- 使用例:
  - Docker 内: docker compose exec backend python /app/scripts/create_journal_via_api.py
  - ローカル: python scripts/create_journal_via_api.py
- 注意:
  - 本番データの直接変更は避ける
  - API URL は .env を参照

### 補足

- 開発環境では Docker volume を利用して、ホスト側のソースコードをコンテナにマウントしています
- バックエンドは `uvicorn --reload`、フロントエンドは Vite の開発サーバーを使用しています
- 本プロジェクトでは Docker 開発を前提としており、Python の仮想環境（`.venv`）は使用しません



## テストアカウント

| ロール | メールアドレス | パスワード |
|--------|---------------|-----------|
| 管理者 | admin@school.ac.jp | password123 |
| 教師（担任） | tanaka.teacher@school.ac.jp | password123 |
| 教師（学年主任） | suzuki.teacher@school.ac.jp | password123 |
| 生徒 | yamada.taro@school.ac.jp | password123 |

## 主要機能

### 生徒機能
- 連絡帳の提出（前登校日の記録を記入）
- 過去の記録の閲覧
- 既読状態の確認

### 教師機能
- クラスの提出状況確認
- 連絡帳の閲覧・既読処理（イイネスタンプ）
- 未読一覧の表示
- 教師メモ（学年共有機能）
- 担当クラスのダッシュボード

### 管理者機能
- ユーザー管理（生徒・教師の作成）
- クラス・学年管理
- システム全体の閲覧権限

## データベース設計

7つの主要テーブルで構成：

- **users**: ユーザー情報（生徒・教師・管理者）
- **grades**: 学年情報（1年・2年・3年）
- **classes**: クラス情報（A組・B組）
- **student_class_assignments**: 生徒のクラス割当（履歴管理対応）
- **teacher_assignments**: 教師の役割・担当割当（担任・学年主任・教科担当）  
  ※ 管理者権限は `users.role = admin` で管理しており、`assignment_type` には含まれません。
- **journal_entries**: 連絡帳エントリ（体調・メンタル・振り返り）
- **teacher_notes**: 教師メモ（学年会議用共有機能）

詳細は `docs/er_diagram.mmd` を参照してください（Mermaid形式）。  
設計の詳細については `docs/design/teacher-assignment-design.md` も参照してください。

## API エンドポイント

### 認証
- `POST /api/auth/login` - ログイン（アクセストークンを返却、リフレッシュトークンは HttpOnly Cookie に保存）
- `GET /api/auth/me` - 現在のユーザー情報取得
- `POST /api/auth/logout` - ログアウト（リフレッシュトークン Cookie を削除）

### 連絡帳
- `POST /api/journals/` - 連絡帳提出
- `GET /api/journals/history` - 履歴取得
- `GET /api/journals/today` - 今日の連絡帳取得
- `GET /api/journals/{id}` - 詳細取得
- `PUT /api/journals/{id}/read` - 既読処理

### 教師機能
- `GET /api/teachers/dashboard` - ダッシュボード情報
- `GET /api/teachers/my-classes` - 担当クラス一覧
- `GET /api/teachers/classes/{class_id}/submissions` - 提出状況(実装予定)
- `GET /api/teachers/unread-journals` - 未読一覧

### ユーザー管理（管理者のみ）
- `POST /api/users/` - ユーザー作成
- `GET /api/users/` - ユーザー一覧取得
- `GET /api/users/{id}` - ユーザー詳細
- `PUT /api/users/{id}` - ユーザー更新
- `DELETE /api/users/{id}` - ユーザー削除

詳細なAPI仕様は http://localhost:8000/docs を参照してください。

## 変更履歴
詳細な変更履歴は [CHANGELOG.md](CHANGELOG.md) を参照してください。

## ドキュメント
設計・仕様・変更履歴の一覧は以下を参照してください。
- docs/INDEX.md