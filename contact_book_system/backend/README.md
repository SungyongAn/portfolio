# Contact Book System - Backend

連絡帳システムのバックエンドサービスです。FastAPIを使用して構築されています。

## 🛠 技術スタック

-   **言語**: Python 3.12
-   **フレームワーク**: FastAPI
-   **ORM**: SQLAlchemy
-   **データベース**: MySQL 8.4
-   **認証**: JWT (JSON Web Tokens)
-   **テスト**: pytest

## 📂 ディレクトリ構成

-   `app/`: アプリケーションのソースコード
    -   `api/`: APIルーター
    -   `models/`: SQLAlchemyモデル
    -   `schemas/`: Pydanticスキーマ
    -   `services/`: ビジネスロジック
    -   `db/`: データベース接続設定
-   `scripts/`: データシードやユーティリティスクリプト
-   `tests/`: テストコード

## 🧪 テストの実行

ルートディレクトリにあるスクリプトを使用してテストを実行します。

```bash
cd ..
./tools/test_backend.sh
```

または、コンテナ内で直接実行することも可能です。

```bash
docker compose exec backend python -m pytest
```
