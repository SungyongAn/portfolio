# 開発案件予実可視化アプリケーション（PoC）

複数のシステムやExcelシートに分散している  
開発案件管理プロセスを一元管理する  
WebアプリケーションのPoC（概念実証）です。

案件申請・承認フロー・進捗管理・予算管理を統合し、

- 開発案件の予実可視化
- KPI監視
- 部門別予実分析
- 危険案件の早期検知
- EVM（SPI / CPI）による健全性監視
- ロール別状況把握

を実現します。

本PoCでは、  
ウォーターフォール型開発案件管理を対象としており、  
実務運用を意識した進捗・予算可視化を重視しています。

---

# デモ環境（評価者向け）

## アプリケーション

http://158.101.148.143

※ モバイル表示はブラウザのレスポンシブモードでも確認可能です。  
※ 動作確認用アカウントは `doc/Information.md` を参照してください。

---

# 課題対応内容

## 課題1（必須）

- 案件申請
- 承認フロー
- 開発進捗管理
- 予算管理

## 課題2（追加提案・実装）

- ウォーターフォール型ガントチャート
- ロール別ダッシュボード
- 部門別分析ダッシュボード
  - 部門別案件数
  - 部門別予算消費率
  - 部門別期限超過件数
- 注視部門ランキング（危険案件・期限超過件数・予算消費率から算出）
- 注視案件一覧（危険理由可視化）
- SPI / CPI によるEVM監視
- TASK_MEMBERロール追加
- モバイル対応
- 今日の対応タスク自動抽出

---

# PoCスコープ

本PoCでは、  
「ウォーターフォール型開発案件の予実可視化」  
を主目的としています。

そのため、

- 詳細なアジャイル運営機能
- ERPレベル予算管理
- 日次工数管理

などは対象外とし、

- 案件申請
- 承認
- KPI可視化
- 進捗監視
- 予算消費状況管理

に重点を置いています。

---

# 技術スタック

## Frontend

- Vue 3
- TypeScript
- Vite
- Pinia
- Vue Router
- Element Plus
- @vueuse/core

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- JWT
- Argon2
- WebSocket
- pytest

## Database

- MySQL 8.0

## Infrastructure

- Docker / Docker Compose
- Oracle Cloud Infrastructure

---

# 機能一覧

## 課題1（必須機能）

- ログイン / ログアウト（JWT認証）
- 案件申請 / 一覧 / 詳細確認
- 承認フロー（申請者 → 部門管理者 → 本部管理者）
- プロジェクトステータス管理
- タスク登録 / 更新 / 削除
- 進捗率管理
- 予算管理
- 工数実績管理
- 直接経費管理
- サーバーサイドページネーション
- フィルター検索

---

## 課題2（追加実装）

### ダッシュボード・KPI監視

- ロール別ダッシュボード
- 部門別分析ダッシュボード
  - 部門別案件数可視化
  - 部門別予算消費率可視化
  - 部門別期限超過件数可視化
- 注視部門ランキング
- 注視案件一覧
  - 危険理由可視化
  - SPI / CPI（簡易EVM）表示
- 今日の対応タスク自動抽出
- KPIカードから案件一覧・承認待ち・危険案件へ直接遷移
- サイドメニューとダッシュボードの導線統一

### タスク管理

- ウォーターフォール型ガントチャート
- タスク詳細Dialogによる画面遷移削減
- TASK_MEMBERロール追加

### 通知機能

- WebSocketによるリアルタイム通知
- PC（Popover）/ スマホ（Drawer）対応通知UI
- 通知詳細Dialogによる一覧維持型UI

### UI・設計改善

- ProjectDetail / BudgetList / TaskForm の責務分離
- View / Component / Composable の責務分離
- レスポンシブ対応

---

# ロール別アクセス制御

| 機能             | APPLICANT | TASK_MEMBER | DEPT_MANAGER | HQ_MANAGER |
| ---------------- | :-------: | :---------: | :----------: | :--------: |
| 案件申請         |    ✅     |      -      |      ✅      |     ✅     |
| 案件閲覧         | 自分のみ  | 自部門のみ  |  自部門のみ  |   全部門   |
| 一次承認         |     -     |      -      |      ✅      |     -      |
| 最終承認         |     -     |      -      |      -       |     ✅     |
| タスク作成・削除 |    ✅     |      -      |      ✅      |     ✅     |
| タスク更新       |    ✅     | 自担当のみ  |      ✅      |     ✅     |
| 予算入力         |    ✅     |      -      |      ✅      |     ✅     |
| 予算閲覧         |     -     |      -      |  自部門のみ  |   全部門   |
| ダッシュボード   |    ✅     |     ✅      |      ✅      |     ✅     |

---

# セットアップ

## 前提

- Docker Desktop

または

- Docker Engine + Compose Plugin

---

## 起動

```bash
git clone <repository-url>
cd quest_1

cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend alembic upgrade head

docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend python -m app.scripts.seed
```

---

## テスト実行

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend pytest tests/ -v
```

---

# ディレクトリ構成

```txt
quest_1/
├── backend/
├── frontend/
├── doc/
│   ├── Information.md
│   ├── user_manual.md
│   ├── er_design.md
│   ├── future_proposals.md
│   └── presentation_*.pdf
├── docker-compose.yml
├── docker-compose.dev.yml
└── docker-compose.prod.yml
```

---

# テストアカウント

詳細は `doc/Information.md` を参照。

---

# リアルタイム通知

- 承認依頼通知
- 却下通知
- 着手通知
- 完了通知
- レビュー依頼通知（将来拡張）

---

# セキュリティ対応

- JWT認証
- Argon2パスワードハッシュ
- ロールベースアクセス制御
- IDOR脆弱性対策
- URL直打ちアクセス制御
- サーバーサイド権限検証

---

# 品質向上対応

- pytest
- Ruff
- TypeScript strict mode
- deploy_check.sh
- SQL集計最適化
- サービス層責務分離
- View / Component / Composable の責務分離

---

# 今後の拡張提案

- 月次進捗報告機能
- 承認ステッパーUI
- CSVエクスポート
- スマホ専用入力画面
- Outlook通知連携
- 監査ログ機能
- Jira / Backlog 連携
- 日次工数管理
- アジャイル案件対応

---

# ドキュメント

`doc/`

- Information.md
- user_manual.md
- er_design.md
- future_proposals.md
- presentation\_{name}.pdf

---

# ライセンス

PoC / 採用インターン提出用
