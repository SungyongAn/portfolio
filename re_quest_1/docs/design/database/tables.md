# tables.md

# テーブル・カラム設計

## 1. テーブル一覧

| テーブル名      | 概要         |
| --------------- | ------------ |
| departments     | 部門情報     |
| users           | ユーザー情報 |
| projects        | 案件情報     |
| project_budgets | 案件予算情報 |
| tasks           | タスク情報   |
| worklogs        | 工数情報     |
| expenses        | 経費情報     |
| notifications   | 通知情報     |

---

# 2. departments

## 概要

部門情報を管理する。

## カラム

| カラム名   | 型           | NULL | 概要     |
| ---------- | ------------ | ---- | -------- |
| id         | BIGINT       | NO   | 主キー   |
| name       | VARCHAR(255) | NO   | 部門名   |
| created_at | DATETIME     | NO   | 作成日時 |
| updated_at | DATETIME     | NO   | 更新日時 |

---

# 3. users

## 概要

システム利用者を管理する。

## カラム

| カラム名      | 型           | NULL | 概要               |
| ------------- | ------------ | ---- | ------------------ |
| id            | BIGINT       | NO   | 主キー             |
| name          | VARCHAR(255) | NO   | ユーザー名         |
| email         | VARCHAR(255) | NO   | メールアドレス     |
| password_hash | VARCHAR(255) | NO   | パスワードハッシュ |
| role          | VARCHAR(50)  | NO   | ロール             |
| department_id | BIGINT       | YES  | 所属部門ID         |
| created_at    | DATETIME     | NO   | 作成日時           |
| updated_at    | DATETIME     | NO   | 更新日時           |

### role

| 値           | 概要       |
| ------------ | ---------- |
| APPLICANT    | 申請者     |
| DEPT_MANAGER | 部門管理者 |
| HQ_MANAGER   | 本部管理者 |
| TASK_MEMBER  | 担当者     |

---

# 4. projects

## 概要

開発案件情報を管理する。

## カラム

| カラム名         | 型            | NULL | 概要               |
| ---------------- | ------------- | ---- | ------------------ |
| id               | BIGINT        | NO   | 主キー             |
| name             | VARCHAR(255)  | NO   | 案件名             |
| description      | TEXT          | YES  | 案件説明           |
| status           | VARCHAR(50)   | NO   | 案件ステータス     |
| department_id    | BIGINT        | NO   | 担当部門ID         |
| applicant_id     | BIGINT        | NO   | 申請者ID           |
| owner_id         | BIGINT        | YES  | 案件責任者ID       |
| start_date       | DATE          | YES  | 開始予定日         |
| end_date         | DATE          | YES  | 終了予定日         |
| budget_amount    | DECIMAL(15,2) | NO   | 予算額             |
| planned_months   | DECIMAL(10,2) | NO   | 予定工数           |
| progress         | INT           | NO   | 進捗率             |
| approval_comment | TEXT          | YES  | 承認・却下コメント |
| created_at       | DATETIME      | NO   | 作成日時           |
| updated_at       | DATETIME      | NO   | 更新日時           |

### status

| 値           | 概要         |
| ------------ | ------------ |
| DRAFT        | 下書き       |
| PENDING_DEPT | 部門承認待ち |
| PENDING_HQ   | 本部承認待ち |
| APPROVED     | 承認済み     |
| IN_PROGRESS  | 進行中       |
| COMPLETED    | 完了         |
| REJECTED     | 却下         |

---

# 5. project_budgets

## 概要

案件ごとの予算・実績情報を管理する。

## カラム

| カラム名         | 型            | NULL | 概要       |
| ---------------- | ------------- | ---- | ---------- |
| id               | BIGINT        | NO   | 主キー     |
| project_id       | BIGINT        | NO   | 案件ID     |
| budget_amount    | DECIMAL(15,2) | NO   | 予算額     |
| unit_price       | DECIMAL(15,2) | NO   | 人月単価   |
| planned_months   | DECIMAL(10,2) | NO   | 予定人月   |
| actual_months    | DECIMAL(10,2) | NO   | 実績人月   |
| actual_cost      | DECIMAL(15,2) | NO   | 実績工数費 |
| expense_cost     | DECIMAL(15,2) | NO   | 経費合計   |
| total_actual     | DECIMAL(15,2) | NO   | 実績合計   |
| consumption_rate | DECIMAL(10,2) | NO   | 予算消化率 |
| created_at       | DATETIME      | NO   | 作成日時   |
| updated_at       | DATETIME      | NO   | 更新日時   |

---

# 6. tasks

## 概要

案件に紐づくタスク情報を管理する。

## カラム

| カラム名    | 型           | NULL | 概要             |
| ----------- | ------------ | ---- | ---------------- |
| id          | BIGINT       | NO   | 主キー           |
| project_id  | BIGINT       | NO   | 案件ID           |
| assignee_id | BIGINT       | YES  | 担当者ID         |
| title       | VARCHAR(255) | NO   | タスク名         |
| description | TEXT         | YES  | タスク説明       |
| status      | VARCHAR(50)  | NO   | タスクステータス |
| progress    | INT          | NO   | 進捗率           |
| start_date  | DATE         | YES  | 開始日           |
| due_date    | DATE         | YES  | 期限日           |
| created_at  | DATETIME     | NO   | 作成日時         |
| updated_at  | DATETIME     | NO   | 更新日時         |

### status

| 値          | 概要       |
| ----------- | ---------- |
| TODO        | 未着手     |
| IN_PROGRESS | 進行中     |
| IN_REVIEW   | レビュー中 |
| DONE        | 完了       |
|             |            |
