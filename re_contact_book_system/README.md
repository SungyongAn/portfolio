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
│   │   ├── dependencies.py  # 認証・依存性注入
│   │   └── main.py          # FastAPIアプリ
│   ├── alembic/             # マイグレーション
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
├── docker-compose.yml       # Docker設定
├── init.sql                 # DB初期化スクリプト
└── docs/
    └── ER図.png
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

```bash
docker exec -i journal_db mysql -uroot -prootpassword < init.sql
```

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
### 補足

- 開発環境では Docker volume を利用して、ホスト側のソースコードをコンテナにマウントしています
- バックエンドは `uvicorn --reload`、フロントエンドは Vite の開発サーバーを使用しています
- 本プロジェクトでは Docker 開発を前提としており、Python の仮想環境（`.venv`）は使用しません



## テストアカウント

| ロール | メールアドレス | パスワード |
|--------|---------------|-----------|
| 管理者 | admin@school.ac.jp | password123 |
| 教師（担任） | tanaka.teacher@school.ac.jcp | password123 |
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
- **journal_entries**: 連絡帳エントリ（体調・メンタル・振り返り）
- **teacher_notes**: 教師メモ（学年会議用共有機能）

詳細は `docs/ER図.png` を参照してください。

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
- `GET /api/teachers/classes/{class_id}/submissions` - 提出状況
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