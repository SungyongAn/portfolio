# API設計

> 課題１の必須機能をもとに、RESTful APIのエンドポイントを定義します。
> BaseURL: `/api`

---

## ■ 認証 `/auth`

| メソッド | エンドポイント  | 説明                 | 対象ロール |
| -------- | --------------- | -------------------- | ---------- |
| POST     | `/auth/login`   | ログイン（JWT発行）  | 全ロール   |
| POST     | `/auth/refresh` | アクセストークン更新 | 全ロール   |

---

## ■ ユーザー `/users`

| メソッド | エンドポイント                        | 説明                         | 対象ロール                              |
| -------- | ------------------------------------- | ---------------------------- | --------------------------------------- |
| GET      | `/users/me`                           | ログイン中のユーザー情報取得 | 全ロール                                |
| GET      | `/users`                              | ユーザー一覧取得             | 全ロール                                |
| GET      | `/users/department/{department_id}`   | 部門別ユーザー一覧取得       | TASK_MEMBER / DEPT_MANAGER / HQ_MANAGER |

### クエリパラメータ（GET `/users`）

| パラメータ    | 型  | 説明               | デフォルト |
| ------------- | --- | ------------------ | ---------- |
| department_id | int | 部門IDで絞り込み   | -          |

---

## ■ 部門 `/departments`

| メソッド | エンドポイント | 説明         | 対象ロール |
| -------- | -------------- | ------------ | ---------- |
| GET      | `/departments` | 部門一覧取得 | 全ロール   |

---

## ■ 案件 `/projects`

| メソッド | エンドポイント                    | 説明                                             | 対象ロール                |
| -------- | --------------------------------- | ------------------------------------------------ | ------------------------- |
| GET      | `/projects`                       | 案件一覧取得（ページネーション・フィルター対応） | 全ロール                  |
| POST     | `/projects`                       | 新規案件申請                                     | APPLICANT                 |
| GET      | `/projects/budget-summary`        | 予算サマリー取得（フィルター連動）               | DEPT_MANAGER / HQ_MANAGER |
| GET      | `/projects/{project_id}`          | 案件詳細取得                                     | 全ロール                  |
| PUT      | `/projects/{project_id}`          | 案件情報更新                                     | APPLICANT                 |
| POST     | `/projects/{project_id}/approve`  | 案件承認・却下                                   | DEPT_MANAGER / HQ_MANAGER |
| PATCH    | `/projects/{project_id}/start`    | 案件着手                                         | APPLICANT（自案件のみ）/ DEPT_MANAGER / HQ_MANAGER |
| PATCH    | `/projects/{project_id}/complete` | 案件完了                                         | DEPT_MANAGER / HQ_MANAGER |

### クエリパラメータ（GET `/projects`）

| パラメータ    | 型       | 説明                               | デフォルト |
| ------------- | -------- | ---------------------------------- | ---------- |
| page          | int      | ページ番号（1以上）                | 1          |
| limit         | int      | 1ページあたりの件数（1〜100）      | 10         |
| status        | string[] | ステータスフィルター（複数指定可） | -          |
| keyword       | string   | 案件名キーワード検索               | -          |
| department_id | int      | 部門IDで絞り込み                   | -          |
| budget_min    | int      | 概算予算の下限（円）               | -          |
| budget_max    | int      | 概算予算の上限（円）               | -          |
| sort_by       | string   | ソート対象（例：`budget_amount`）  | -          |
| sort_order    | string   | ソート順（`asc` / `desc`）         | `desc`     |
| alert_level   | string   | アラートレベル（`danger` / `warning`）| -       |

### 案件一覧レスポンス

| フィールド名 | 型   | 説明                |
| ------------ | ---- | ------------------- |
| total        | int  | 総件数              |
| page         | int  | 現在ページ          |
| limit        | int  | 1ページあたりの件数 |
| items        | list | 案件一覧            |

---

## ■ タスク管理 `/projects/{project_id}/tasks`

| メソッド | エンドポイント                           | 説明           | 対象ロール                          |
| -------- | ---------------------------------------- | -------------- | ----------------------------------- |
| GET      | `/projects/{project_id}/tasks`           | タスク一覧取得 | 全ロール                            |
| POST     | `/projects/{project_id}/tasks`           | タスク登録     | APPLICANT / DEPT_MANAGER            |
| PUT      | `/projects/{project_id}/tasks/{task_id}` | タスク更新     | APPLICANT / DEPT_MANAGER / TASK_MEMBER（自部門・進行中まで） |
| DELETE   | `/projects/{project_id}/tasks/{task_id}` | タスク削除     | APPLICANT / DEPT_MANAGER            |

---

## ■ 予算管理 `/projects/{project_id}/budget`

| メソッド | エンドポイント                  | 説明         | 対象ロール |
| -------- | ------------------------------- | ------------ | ---------- |
| GET      | `/projects/{project_id}/budget` | 予算情報取得 | 全ロール   |
| POST     | `/projects/{project_id}/budget` | 予算登録     | APPLICANT  |
| PUT      | `/projects/{project_id}/budget` | 予算更新     | APPLICANT  |

---

## ■ 工数実績 `/projects/{project_id}/worklogs`

| メソッド | エンドポイント                                 | 説明                 | 対象ロール |
| -------- | ---------------------------------------------- | -------------------- | ---------- |
| GET      | `/projects/{project_id}/worklogs`              | 工数実績一覧取得     | 全ロール   |
| POST     | `/projects/{project_id}/worklogs`              | 工数実績登録（月次） | APPLICANT  |
| PUT      | `/projects/{project_id}/worklogs/{worklog_id}` | 工数実績更新         | APPLICANT  |
| DELETE   | `/projects/{project_id}/worklogs/{worklog_id}` | 工数実績削除         | APPLICANT  |

---

## ■ 直接経費 `/projects/{project_id}/expenses`

| メソッド | エンドポイント                                 | 説明             | 対象ロール |
| -------- | ---------------------------------------------- | ---------------- | ---------- |
| GET      | `/projects/{project_id}/expenses`              | 直接経費一覧取得 | 全ロール   |
| POST     | `/projects/{project_id}/expenses`              | 直接経費登録     | APPLICANT  |
| PUT      | `/projects/{project_id}/expenses/{expense_id}` | 直接経費更新     | APPLICANT  |
| DELETE   | `/projects/{project_id}/expenses/{expense_id}` | 直接経費削除     | APPLICANT  |

---

## ■ ダッシュボード `/dashboard`

| メソッド | エンドポイント      | 説明                                         | 対象ロール |
| -------- | ------------------- | -------------------------------------------- | ---------- |
| GET      | `/dashboard`        | ダッシュボードサマリー取得（ロール別集計）   | 全ロール   |
| GET      | `/dashboard/alerts` | アラート案件一覧取得                         | 全ロール   |

---

## ■ 管理タスク `/tasks`

| メソッド | エンドポイント | 説明                               | 対象ロール  |
| -------- | -------------- | ---------------------------------- | ----------- |
| GET      | `/tasks/all`   | 全案件のタスク一覧取得（横断確認） | HQ_MANAGER  |

---

## ■ 通知 `/notifications`

| メソッド  | エンドポイント                          | 説明                                 | 対象ロール |
| --------- | --------------------------------------- | ------------------------------------ | ---------- |
| GET       | `/notifications`                        | 通知一覧取得（ページネーション対応） | 全ロール   |
| PUT       | `/notifications/{notification_id}/read` | 通知を既読にする                     | 全ロール   |
| PUT       | `/notifications/read-all`               | 全通知を既読にする                   | 全ロール   |
| WebSocket | `/notifications/ws?token={token}`       | リアルタイム通知                     | 全ロール   |

### クエリパラメータ（GET `/notifications`）

| パラメータ | 型  | 説明                          | デフォルト |
| ---------- | --- | ----------------------------- | ---------- |
| page       | int | ページ番号（1以上）           | 1          |
| limit      | int | 1ページあたりの件数（1〜100） | 10         |

---

## ■ 案件ステータス定義

| ステータス   | 説明               | 遷移元                    | 遷移先                |
| ------------ | ------------------ | ------------------------- | --------------------- |
| DRAFT        | 下書き（未申請）   | -                         | PENDING_DEPT          |
| PENDING_DEPT | 部門管理者承認待ち | DRAFT                     | PENDING_HQ / REJECTED |
| PENDING_HQ   | 本部管理者承認待ち | PENDING_DEPT              | APPROVED / REJECTED   |
| APPROVED     | 承認済み           | PENDING_HQ                | IN_PROGRESS           |
| IN_PROGRESS  | 進行中             | APPROVED                  | COMPLETED             |
| COMPLETED    | 完了               | IN_PROGRESS               | -                     |
| REJECTED     | 却下               | PENDING_DEPT / PENDING_HQ | -                     |

---

## ■ タスクステータス定義

| ステータス  | 説明       |
| ----------- | ---------- |
| TODO        | 未着手     |
| IN_PROGRESS | 進行中     |
| IN_REVIEW   | レビュー中 |
| DONE        | 完了       |

---

## ■ 主なエラーコード

| コード | HTTPステータス        | 説明                                 |
| ------ | --------------------- | ------------------------------------ |
| 400    | Bad Request           | 入力値エラー・ステータス遷移エラー   |
| 401    | Unauthorized          | 認証エラー                           |
| 403    | Forbidden             | 権限エラー                           |
| 404    | Not Found             | リソースが存在しない                 |
| 409    | Conflict              | 重複登録エラー（同一月の工数実績等） |