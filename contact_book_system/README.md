# 連絡帳管理システム

公立中学校向けのデジタル連絡帳管理システム

## 主な機能

- JWT 認証とロールベースのアクセス制御
- デジタル連絡帳（日々の記録、健康状態、学習記録）
- WebSocket リアルタイムチャット
- アカウント管理（メールアドレスベース）
- 卒業生データの自動アーカイブ（3 ～ 5 年保管）

## 技術スタック

| カテゴリ           | 技術                                    |
| :----------------- | :-------------------------------------- |
| **フロントエンド** | Vue.js 3, Vite, Vue Router, Bootstrap 5 |
| **バックエンド**   | Python 3.12, FastAPI, SQLAlchemy        |
| **データベース**   | MySQL 8.4                               |
| **インフラ**       | Docker, Docker Compose                  |

## ディレクトリ構成

```
.
├── backend/          # FastAPI バックエンド
│   ├── app/          # アプリケーションコード (api/model/repository/schema/service)
│   └── scripts/      # ユーティリティスクリプト
├── frontend/         # Vue.js フロントエンド
│   └── src/          # ソースコード (components/router)
├── tools/            # セットアップ・テストスクリプト
└── docker-compose.yml
```

## セットアップ

### 開発環境（サンプルデータあり）

```bash
./tools/setup_dev.sh
```

### 本番環境（管理者のみ）

```bash
./tools/setup_prod.sh
```

### 通常起動

```bash
docker compose up -d
```

## アクセス

- **フロントエンド**: http://localhost:5173
- **バックエンド API**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs

## ログイン情報（開発用）

| ロール   | ID       | パスワード |
| :------- | :------- | :--------- |
| 管理者   | admin    | admin123   |
| 養護教諭 | tanaka.h | nurse123   |
| 教師     | sato.t   | teacher123 |
| 生徒     | aoki.i   | student123 |

**注**: ログイン時は`@school.local`より前の部分のみを入力

## 管理コマンド

```bash
# パスワード一括リセット
docker compose exec backend python scripts/update_passwords.py

# ログ確認
docker compose logs

# 再構築
docker compose down
docker compose up -d --build
```

## 自動処理スケジュール

毎年 4 月 1 日に以下が自動実行されます：

- **午前 1 時**: 学年進級・卒業処理
- **午前 2 時**: 連絡帳アーカイブ
- **午前 3 時**: 保管期限切れデータ削除

## 詳細ドキュメント

- [バックエンド](./backend/README.md)
- [フロントエンド](./frontend/README.md)
- [変更履歴](./CHANGELOG.md)
