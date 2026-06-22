# S-APP-03：案件詳細画面

## ■ 目的

案件の詳細情報・進捗・予算を確認し、各種操作の起点となる

---

## ■ 対象ロール

- 全ロール

---

## ■ 業務上の役割

案件の詳細確認・各種操作の起点

---

## ■ 表示項目

| 項目             | 説明                                                                     |
| ---------------- | ------------------------------------------------------------------------ |
| 案件名           |                                                                          |
| ステータス       | タグ形式で色分け表示                                                     |
| 概算予算（円）   |                                                                          |
| 概算工数（人月） |                                                                          |
| 開発開始予定日   |                                                                          |
| 完了予定日       |                                                                          |
| 進捗率           | 配下タスクの平均で自動算出・プログレスバー表示                           |
| アラートレベル   | danger / warning をタグ表示                                              |
| タスク一覧       | タスク名・担当者・ステータス・進捗率・開始日・期限（ガントチャート表示） |
| 予算サマリ       | 予算額・実績額・消化率（ProjectBudgetResponseから取得）                  |

---

## ■ 操作

| 操作       | 内容                                     | 条件                                                                 |
| ---------- | ---------------------------------------- | -------------------------------------------------------------------- |
| 案件編集   | 案件情報編集画面へ遷移                   | APPLICANT / DEPT_MANAGER / HQ_MANAGER                                |
| 承認・却下 | 承認・却下画面へ遷移                     | DEPT_MANAGER / HQ_MANAGERのみ・承認待ち案件のみ                      |
| 着手       | 案件ステータスをIN_PROGRESSへ変更        | APPLICANT（自案件のみ）/ DEPT_MANAGER / HQ_MANAGER・APPROVED案件のみ |
| 完了       | 案件ステータスをCOMPLETEDへ変更          | DEPT_MANAGER / HQ_MANAGER・IN_PROGRESS案件のみ                       |
| タスク登録 | タスク登録画面（S-TSK-01）へ遷移         | APPLICANTのみ・承認済み案件のみ                                      |
| タスク更新 | タスク更新Dialog（インライン表示）を開く | APPLICANT / TASK_MEMBER・承認済み案件のみ                            |
| 予算管理   | 予算管理画面（S-BDG-01）へ遷移           | APPLICANT / DEPT_MANAGER / HQ_MANAGER                                |

---

## ■ バリデーション / 制御

- ロールに応じてアクセス可能な案件を制御
  - APPLICANT：自身の案件のみ
  - TASK_MEMBER：自部門の案件のみ
  - DEPT_MANAGER：自部門の案件のみ
  - HQ_MANAGER：全部門の案件
- 承認前ステータス（DRAFT / PENDING_DEPT / PENDING_HQ / REJECTED）の案件では予算・タスクを非表示

---

## ■ 画面遷移

- 遷移元：案件一覧画面（S-APP-01）・ダッシュボード（S-CMN-01）
- 遷移先：
  - 承認・却下画面（S-APR-01）
  - タスク登録画面（S-TSK-01）
  - 予算管理画面（S-BDG-01）
- インライン表示（画面遷移なし）：
  - タスク更新Dialog

---

## ■ 使用API

| メソッド | エンドポイント                         | 説明                 |
| -------- | -------------------------------------- | -------------------- |
| GET      | /projects/{project_id}                 | 案件詳細取得         |
| GET      | /projects/{project_id}/tasks           | タスク一覧取得       |
| GET      | /projects/{project_id}/budget          | 予算サマリ取得       |
| PUT      | /projects/{project_id}/tasks/{task_id} | タスク更新（Dialog） |
| PATCH    | /projects/{project_id}/start           | 案件着手             |
| PATCH    | /projects/{project_id}/complete        | 案件完了             |

---

## ■ 備考

- タスク更新はインラインDialog（TaskDetailDialog）で完結し、専用画面への遷移は行わない
- タスク登録のみ専用画面（S-TSK-01）へ遷移する
- 予算サマリはProjectBudgetResponseのフィールドから取得・表示する
- 承認前ステータスの案件で予算APIが404を返す場合は正常系として処理する
