# 野球部タレントマネジメントシステム PoC
## プレゼンテーション資料

---

## 1. プロジェクト概要

### システム概要
神奈川県立JPT高校野球部の測定記録管理業務をWebアプリケーションとして実現したPoCです。

### 技術スタック
| レイヤー | 技術 |
|---------|------|
| フロントエンド | Vue 3 / Vite / Pinia / Bootstrap / ECharts |
| バックエンド | FastAPI / SQLAlchemy / Alembic |
| データベース | MySQL 8.0 |
| 認証 | JWT（Access Token + Refresh Token） / Argon2 |
| インフラ | Docker / docker-compose / Oracle Cloud（Ubuntu 22.04） |

---

## 2. 課題1：工夫点・アピール

### 2.1 設計面の工夫

#### 3層アーキテクチャの採用
```
routers（エンドポイント定義）
  └── services（ビジネスロジック + DBアクセス）
        └── crud（将来の拡張用・今回はservicesに統合）
```
PoCの規模に合わせてcrud層の分離を将来の拡張として意図的に保留し、最小構成で動作するアーキテクチャを選択しました。

#### セキュリティを考慮した認証設計
- **Access Token**：メモリのみで管理（XSS対策）
- **Refresh Token**：HttpOnly Cookieで管理（XSS対策）
- **tokenExpiry**：sessionStorageで管理（リロード時の認証状態復元用）

リロード時にAccess Tokenが失われても、Refresh Tokenで自動復元する仕組みを実装しました。

#### Python側でのタイムスタンプ管理
`onupdate=sa.func.now()`がMySQLで効かないケースがあることを把握し、`datetime.now(timezone.utc)`でPython側から明示的に管理する方針を採用しました。

#### インデックス設計
頻繁に発生するクエリを分析し、以下のインデックスを設計・実装しました。

| テーブル | インデックス | 理由 |
|---------|------------|------|
| users | ix_users_role | ロール別部員一覧取得に使用 |
| users | ix_users_status | 在籍中の部員絞り込みに使用 |
| measurements | ix_measurements_user_id | 部員別測定記録取得（既存） |
| measurements | ix_measurements_status | 承認フローの絞り込みに使用 |
| measurements | ix_measurements_measurement_date | 計測日での絞り込みに使用 |
| measurements | ix_measurements_user_id_measurement_date | 重複チェック用複合インデックス |

### 2.2 実装面の工夫

#### ロール別アクセス制御の二重化
- **バックエンド**：JWTトークンのロール検証（`require_roles`依存性注入）
- **フロントエンド**：Vue Routerのナビゲーションガード

フロントエンドのガードだけでは不十分なため、バックエンドでも制御することでセキュリティを担保しました。

#### 承認フローのステータス設計
```
draft → pending_member → pending_coach → approved
                    ↓               ↓
                rejected        rejected
```
各ステータスで操作できるロールを明確に分離し、不正な遷移を防ぐバリデーションをサービス層に実装しました。

#### Axiosインターセプターによるトークン自動更新
401エラー発生時にRefresh Tokenで自動更新し、元のリクエストを再送する処理を実装しました。また`/api/auth/refresh`自体が401を返した場合の無限ループを防ぐ処理も追加しました。

#### フロントエンドのcomputedパターン統一
`ref`と`computed`の使い分けを明確に定義しました。
- `ref`：ユーザー操作で変化する値（showModal・loading など）
- `computed`：既存データから派生する値（フィルタリング結果など）

### 2.3 トラブルシューティング

| 問題 | 原因 | 解決策 |
|------|------|--------|
| Dockerネットワーク通信不可 | docker-compose.ymlにnetworks設定がなかった | app-networkを追加 |
| alembicマイグレーション失敗 | DATABASE_URLの設定がコメントアウトされていた | コメントアウトを解除 |
| リロードでログアウト | PiniaのstateはリロードでリセットされるためaccessTokenが消える | tokenExpiryをsessionStorageに保存し認証状態を復元 |
| 401の無限ループ | /api/auth/refreshの401もインターセプターが再試行していた | refreshエンドポイントの場合はループしない処理を追加 |
| node_modulesが上書き | ホスト側マウントとコンテナ内node_modulesが競合 | Dockerfileのボリューム設定を調整 |

---

## 3. 課題2：提案内容

### 3.1 提案の背景

課題PDFのヒアリング結果・モックUI操作時の気づきを根拠として提案を策定しました。

| ヒアリング対象 | 課題 | 提案 |
|-------------|------|------|
| 監督・コーチ | チーム全体の傾向把握が困難 | ECharts可視化ダッシュボード |
| 監督・コーチ | メッセージ記録手段がない | メッセージ機能（技術証明） |
| 部員 | 自分のチーム内位置づけが不明 | チーム内順位・レーダーチャート |
| 部員 | スマホで操作したい | スマートフォン対応（技術証明） |
| 部員 | 測定項目を変えたい | 測定項目の柔軟化（技術証明） |
| マネージャー | 登録操作が多い | 確認モーダル・将来の一括処理 |
| マネージャー | 入力ミスが怖い | 重複登録防止・確認フロー |
| マネージャー | 承認状況をリアルタイムで把握したい | ダッシュボード通知・WebSocketリアルタイム通知（技術証明） |

### 3.2 実装済み機能

#### 重複登録防止
- 同一部員・同一計測日の重複チェックをバックエンドに追加
- `rejected`レコードは上書き更新して`draft`に戻す設計
- 登録前の確認モーダルを追加（マネージャーのミス防止）

#### 可視化ダッシュボード（ECharts）
4つのグラフをタブ切り替えで表示します。

| グラフ | 対象ロール | 内容 |
|--------|----------|------|
| 成長推移（折れ線） | 全ロール | チーム平均・個人の時系列推移 |
| 能力比較（レーダー） | コーチ・監督 | 部員間の能力比較・チーム平均比較 |
| チーム内順位（テーブル） | 全ロール | 測定項目別の順位表・自分の位置づけ |

#### 測定結果閲覧画面の改善
- ソート・絞り込み・ページネーション機能を全画面に追加
- フィルタ・ソート条件のURLクエリパラメータ同期（ブラウザバック対応）

#### コンポーネント責務分離
- composablesパターンでデータ加工ロジックをUIから分離
- `measurement/`・`member/`・`visualization/`配下にコンポーネントを整理

### 3.3 技術証明（未実装機能）

実装時間の制約から以下の機能は技術的根拠のみ示します。

#### マネージャー入力履歴管理
`measurements`テーブルに`created_by`カラムを追加するマイグレーションで対応可能です。
```python
# alembic migration
op.add_column('measurements', 
    sa.Column('created_by', sa.Integer(), 
    sa.ForeignKey('users.id'), nullable=True))
```

#### ポジション管理・ポジション別比較
`users`テーブルに`position`カラムを追加し、可視化ダッシュボードのフィルターに組み込む形で拡張可能です。

#### スマートフォン対応
Bootstrapのレスポンシブユーティリティクラス（`d-none d-md-block`等）と`table-responsive`の活用で対応可能です。テーブルの横スクロール対応が主な実装箇所になります。

#### パスワード変更機能
```python
# backend
@router.patch("/api/users/{user_id}/password")
def update_password(user_id: int, request: PasswordUpdateRequest):
    # 現在のパスワード検証 → 新パスワードのハッシュ化 → 更新
```

#### ダッシュボード通知機能
各ロールのダッシュボードに承認状況のサマリーを表示します。
表示データは既存の `getMeasurements()` APIの取得済みデータをフロントエンド側で集計するため、APIの追加は不要です。

| ロール | 表示内容 |
|--------|---------|
| マネージャー | 否認件数・部員承認待ち件数・コーチ承認待ち件数 |
| 部員 | 自身への承認依頼の有無（`pending_member` レコードの存在） |
| コーチ | 承認依頼の受信件数（`pending_coach` レコードの件数） |

#### WebSocketによるリアルタイム通知
承認フローのステータス変化をWebSocketでリアルタイムに通知します。アプリ使用中に承認依頼や承認完了が発生した際、画面遷移なしで即座に把握できます。

| イベント | 通知先 |
|---------|--------|
| マネージャーが承認フロー発行 | 対象部員 |
| 部員が承認 | コーチ全員 |
| コーチが承認・否認 | マネージャー全員・対象部員 |

- **認証**：WebSocketはHTTPヘッダーを使用できないため、クエリパラメータでAccess Tokenを渡し接続時にJWT検証を行う
- **本番運用時の考慮**：複数ワーカー構成ではRedis Pub/Subなどのメッセージブローカーの導入が必要

#### 承認済みレコードの確認済み管理
`MeasurementStatusList`にてコーチ承認済みレコードを「確認」ボタンで非表示にできる機能です。
確認状態は`measurements`テーブルの`manager_confirmed`カラム（BOOLEAN）に永続化し、複数デバイス・複数マネージャー間で状態を共有します。

localStorageによるフロントエンド管理でも機能検証は可能ですが、複数デバイス・複数マネージャーが使う実運用を想定し、DBへの永続化を設計として選択しました。

### 3.4 運用ルール整備提案

| ルール | 内容 |
|--------|------|
| 入力ルール | 測定日当日または翌日までに入力・承認フローを発行 |
| 承認ルール | 部員は2営業日以内・コーチは部員承認後2営業日以内に対応 |
| アカウント管理 | マネージャーは個別アカウント使用（共有禁止） |
| 測定日ルール | 2か月に1度・同一部員・同一計測日の重複登録禁止 |

---

## 4. デプロイ環境

### 環境情報
- **クラウド**：Oracle Cloud Always Free（Ubuntu 22.04）
- **URL**：`http://168.138.193.7/`
- **構成**：docker-compose（nginx + FastAPI + MySQL）

### アクセス方法
テストアカウント一覧（`docs/test_accounts.md`）を参照してください。

### デプロイ手順概要
```bash
# 1. リポジトリのクローン
git clone <repository_url>
cd baseball_talent_manager

# 2. 本番環境の起動
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# 3. マイグレーション実行
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec backend alembic upgrade head

# 4. 初期データ投入
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec db mysql -uroot -proot baseball_talent_manager < seed.sql
```

---

## 5. 課題・インターンの感想

<!-- ここに感想を記入してください -->

### 課題を通じて学んだこと


### 難しかった点


### 今後に活かしたいこと


---

## 6. 参考資料

- 提案書詳細：`docs/proposal.md`
- テストアカウント一覧：`docs/test_accounts.md`
- API設計：`docs/api.md`
- ER図：`docs/er.md`
- 認証設計：`docs/auth_design.md`