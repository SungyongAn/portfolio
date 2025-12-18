# バックエンド

FastAPI ベースの RESTful API サーバー

## 技術スタック

- **言語**: Python 3.12
- **フレームワーク**: FastAPI
- **ORM**: SQLAlchemy
- **認証**: JWT (python-jose)
- **パスワード**: bcrypt (passlib)
- **DB**: MySQL 8.4

## ディレクトリ構成

```
backend/
├── app/
│   ├── api/          # APIエンドポイント
│   ├── model/        # データベースモデル
│   ├── repository/   # データアクセス層
│   ├── schema/       # リクエスト/レスポンススキーマ
│   ├── service/      # ビジネスロジック
│   ├── db.py         # DB接続設定
│   └── main.py       # エントリーポイント
└── scripts/          # ユーティリティスクリプト
```

## 環境構築

### ローカル

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker compose up -d
```

## 主要 API

| エンドポイント         | メソッド | 説明               | 認証         |
| :--------------------- | :------- | :----------------- | :----------- |
| `/api/auth/login`      | POST     | ログイン           | 不要         |
| `/api/accounts`        | POST     | アカウント登録     | 必要         |
| `/api/accounts/search` | GET      | アカウント検索     | 必要         |
| `/api/renrakucho`      | POST/GET | 連絡帳作成/取得    | 必要         |
| `/api/chat/rooms`      | GET      | チャットルーム一覧 | 必要         |
| `/ws/chat/{room_id}`   | WS       | WebSocket 接続     | 必要         |
| `/api/archive/execute` | POST     | アーカイブ実行     | 必要(管理者) |

**API ドキュメント**: http://localhost:8000/docs

## 認証

### ログイン方式

- メールアドレス + パスワード
- フロントエンドからローカルパート送信 → バックエンドで`@school.local`付与

### JWT 構成

```json
{
  "sub": "user@school.local",
  "role": "teacher",
  "user_id": 3,
  "exp": 1234567890
}
```

### ロール別権限

- **admin**: 全機能、アカウント管理、アーカイブ管理
- **teacher**: 担当クラスの連絡帳、チャット
- **student**: 自分の連絡帳、クラスチャット
- **nurse**: 全生徒の健康状態、専用チャット

## データベース

### 主要テーブル

- `accounts`: アカウント情報
- `renrakucho_entries`: 連絡帳
- `renrakucho_entries_archive`: アーカイブ（3 ～ 5 年保管）
- `chat_messages`: チャットメッセージ
- `data_deletion_log`: 削除ログ

### ストアドプロシージャ

- `archive_old_renrakucho(years)`: 古い連絡帳をアーカイブ
- `delete_expired_renrakucho(retention_years)`: 期限切れデータ削除
- `get_archive_statistics()`: 統計取得

### スケジュールイベント

- `promote_students`: 毎年 4/1 1:00 学年進級・卒業
- `yearly_archive_renrakucho`: 毎年 4/1 2:00 アーカイブ
- `yearly_delete_expired_renrakucho`: 毎年 4/1 3:00 期限切れ削除

## WebSocket 通信

### 接続

```
ws://localhost:8000/ws/chat/{room_id}?token={jwt_token}
```

### メッセージ形式

```json
// 送信
{"type": "message", "content": "text", "room_id": "class_1_1"}
{"type": "typing", "is_typing": true}

// 受信
{"type": "message", "sender_id": 3, "content": "text", "timestamp": "..."}
{"type": "user_status", "user_id": 5, "status": "online"}
```

## 開発ガイド

### 新規 API エンドポイント追加

1. **スキーマ定義** (`schema/`)
2. **モデル定義** (`model/`)
3. **リポジトリ** (`repository/`)
4. **サービス** (`service/`)
5. **API エンドポイント** (`api/`)
6. **main.py に登録**

### コードフォーマット

```bash
black app/
isort app/
flake8 app/
```

## 参考資料

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
