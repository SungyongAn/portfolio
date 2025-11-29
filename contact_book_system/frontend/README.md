# Contact Book System - Frontend

連絡帳システムのフロントエンドアプリケーションです。Vue.js 3とViteを使用して構築されています。

## 🛠 技術スタック

-   **フレームワーク**: Vue.js 3 (Options API)
-   **ビルドツール**: Vite
-   **UIフレームワーク**: Bootstrap 5
-   **HTTPクライアント**: Axios
-   **テスト**: Vitest, Vue Test Utils

## 📂 ディレクトリ構成

-   `src/`: ソースコード
    -   `components/`: Vueコンポーネント
        -   `AccountManagement/`: アカウント管理関連
        -   `Renrakucho/`: 連絡帳関連
        -   `__tests__/`: テストコード
    -   `assets/`: 静的リソース
-   `vite.config.js`: Vite設定ファイル

## 🧪 テストの実行

ルートディレクトリにあるスクリプトを使用してテストを実行します。

```bash
cd ..
./tools/test_frontend.sh
```

または、コンテナ内で直接実行することも可能です。

```bash
docker compose exec frontend npm test
```
