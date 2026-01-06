# 連絡帳管理システム

学校向け連絡帳のデジタル管理システム。生徒の日々の記録を効率的に管理し、教師との円滑なコミュニケーションを実現します。

## 技術スタック

### Backend
- **Framework**: FastAPI 0.115.5
- **Database**: MySQL 8.0 (Docker)
- **ORM**: SQLAlchemy 2.0.36
- **Migration**: Alembic 1.14.0
- **Authentication**: JWT (python-jose 3.3.0 + passlib 1.7.4 + bcrypt 5.0.0)
- **Python**: 3.11.9
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
│   ├── .venv/               # 仮想環境 (uv)
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

## セットアップ

### 前提条件

- **Python**: 3.11.9
- **Node.js**: 18+
- **Docker Desktop**: 最新版
- **uv**: Python package manager（高速な依存関係管理）

#### uvのインストール
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 確認
uv --version
```

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd re_contact_book_system
```

### 2. バックエンドのセットアップ
```bash
cd backend

# Python 3.11.9 で仮想環境を作成
uv venv --python 3.11.9

# 仮想環境を有効化
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Mac/Linux:
source .venv/bin/activate

# 依存関係をインストール (uvを使用)
uv pip install -r requirements.txt

# インストール確認
uv pip list

# 環境変数ファイルを作成
cp .env.example .env
# .env を編集して環境に合わせた設定を記入
```

**インストールされる主要パッケージ (44パッケージ)**:
- FastAPI 0.115.5
- Uvicorn 0.32.1
- SQLAlchemy 2.0.36
- PyMySQL 1.1.1
- Alembic 1.14.0
- Pydantic 2.10.4
- python-jose 3.3.0
- passlib 1.7.4
- bcrypt 5.0.0
- email-validator 2.2.0

### 3. データベースのセットアップ
```bash
# MySQLコンテナを起動
docker-compose up -d

# 起動確認
docker ps

# データベースを初期化
docker exec -i journal_db mysql -uroot -prootpassword < init.sql

# 接続確認
python test_db_connection.py
```

### 4. バックエンドの起動
```bash
cd backend

# 仮想環境が有効化されていることを確認
# プロンプトに (.venv) が表示されていればOK

# サーバー起動
uvicorn app.main:app --reload
```

**起動確認**:
- サーバー: http://localhost:8000
- API ドキュメント (Swagger UI): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. フロントエンドのセットアップ
```bash
cd frontend

# 依存関係をインストール
npm install

# 環境変数ファイルを作成
echo "VITE_API_URL=http://localhost:8000" > .env

# 開発サーバーを起動
npm run dev
```

フロントエンドは http://localhost:5173 で起動します。

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
- **journal_entries**: 連絡帳エントリ（体調・メンタル・振り返り）
- **teacher_notes**: 教師メモ（学年会議用共有機能）

詳細は `docs/ER図.png` を参照してください。

## API エンドポイント

### 認証
- `POST /api/auth/login` - ログイン（JWT発行）
- `GET /api/auth/me` - 現在のユーザー情報取得
- `POST /api/auth/logout` - ログアウト

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

## トラブルシューティング

### バックエンドが起動しない
```bash
# 仮想環境が有効化されているか確認
# プロンプトに (.venv) が表示されているか確認

# Windowsの場合
where python
# 出力: C:\...\backend\.venv\Scripts\python.exe

# uvでパッケージを再インストール
uv pip install -r requirements.txt

# データベース接続を確認
python test_db_connection.py
```

### uvコマンドが見つからない
```bash
# uvを再インストール
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# パスが通っているか確認
uv --version
```

### フロントエンドでCORSエラー

`backend/app/main.py` のCORS設定を確認：
```python
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

バックエンドを再起動してください。

### データベース接続エラー
```bash
# Dockerコンテナが起動しているか確認
docker ps

# journal_db が表示されない場合
docker-compose up -d

# MySQLに直接接続して確認
docker exec -it journal_db mysql -uroot -prootpassword journal_system

# ユーザーが存在するか確認
SELECT email, name, role FROM users;
```

### bcryptのバージョン問題

Python 3.11.9 + bcrypt 5.0.0 の組み合わせで正常動作を確認済み。
もしエラーが出る場合は仮想環境を再作成してください：
```bash
# 仮想環境を削除
Remove-Item -Recurse -Force .venv

# 再作成
uv venv --python 3.11.9
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

## 変更履歴

詳細な変更履歴は [CHANGELOG.md](CHANGELOG.md) を参照してください。