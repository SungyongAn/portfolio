# tasks（タスク）

## カラム

| カラム名    | 型                                            | NULL | デフォルト                  | 説明                                 |
| ----------- | --------------------------------------------- | ---- | --------------------------- | ------------------------------------ |
| id          | INT                                           | NO   | AUTO_INCREMENT              | タスクID                             |
| project_id  | INT                                           | NO   | -                           | 案件ID                               |
| assignee_id | INT                                           | YES  | NULL                        | 担当者ID                             |
| name        | VARCHAR(200)                                  | NO   | -                           | タスク名                             |
| phase_name  | VARCHAR(100)                                  | YES  | NULL                        | 工程名（ウォーターフォール工程区分） |
| description | TEXT                                          | YES  | NULL                        | タスク説明                           |
| status      | ENUM('TODO','IN_PROGRESS','IN_REVIEW','DONE') | NO   | 'TODO'                      | ステータス                           |
| progress    | INT                                           | NO   | 0                           | 進捗率（%）                          |
| start_date  | DATE                                          | YES  | NULL                        | 開始日                               |
| due_date    | DATE                                          | YES  | NULL                        | 期限                                 |
| created_at  | DATETIME                                      | NO   | CURRENT_TIMESTAMP           | 作成日時                             |
| updated_at  | DATETIME                                      | NO   | CURRENT_TIMESTAMP ON UPDATE | 更新日時                             |

## インデックス

```sql
PRIMARY KEY (id)
INDEX idx_tasks_project_id (project_id)
INDEX idx_tasks_assignee_id (assignee_id)
INDEX idx_tasks_project_status (project_id, status)
INDEX idx_tasks_assignee_status (assignee_id, status)
INDEX idx_tasks_due_date (due_date)
```

## 制約

```sql
FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE SET NULL
CHECK (progress BETWEEN 0 AND 100)
```

## 変更点

- `parent_task_id` 削除（階層構造を廃止）
- `level` 削除（階層構造を廃止）
- `planned_hours` / `actual_hours` 削除（工数管理は worklogs・project_budgets で管理）
- `note` / `sort_order` 削除（実装なし）
- `phase_name` / `description` 追加（ウォーターフォール工程管理・タスク説明）
- `status` Enum を `TODO` / `IN_PROGRESS` / `IN_REVIEW` / `DONE` に統一

## 備考

- phase_name について
  - ウォーターフォール型開発における工程分類を想定（例：要件定義・基本設計・詳細設計・実装・テスト・リリース）
  - ガントチャートの工程別表示・並び替えに使用する

- status と progress の連動ルール
  - ステータスを `DONE` にすると progress が 100 に自動設定される
  - progress を 100 にするとステータスが `DONE` に自動設定される
  - 案件全体の進捗率は配下タスクの progress 平均値で自動算出する
