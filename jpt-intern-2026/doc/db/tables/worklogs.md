# worklogs（工数実績）

## カラム

| カラム名      | 型           | NULL | デフォルト                  | 説明                  |
| ------------- | ------------ | ---- | --------------------------- | --------------------- |
| id            | INT          | NO   | AUTO_INCREMENT              | 工数実績ID            |
| project_id    | INT          | NO   | -                           | 案件ID                |
| work_month    | VARCHAR(7)   | NO   | -                           | 対象月（例：2026-04） |
| actual_months | DECIMAL(5,2) | NO   | 0.00                        | 実績工数（人月）      |
| created_at    | DATETIME     | NO   | CURRENT_TIMESTAMP           | 作成日時              |
| updated_at    | DATETIME     | NO   | CURRENT_TIMESTAMP ON UPDATE | 更新日時              |

## インデックス

```sql
PRIMARY KEY (id)
INDEX idx_worklogs_project_id (project_id)
INDEX idx_worklogs_work_month (work_month)
UNIQUE INDEX uq_worklog_project_month (project_id, work_month)
```

## 制約

```sql
FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
```

## 変更点

- `task_id` 削除（工数は案件単位で管理）
- `user_id` 削除（工数は案件単位で管理・個人別管理は課題２）
- `work_date` → `work_month` に変更（日次→月次）
- カラム名 `hours` → `actual_months` に変更（人月単位であることを明示）
- `note` 削除（実装なし）
- ユニーク制約を `(project_id, work_month)` に変更（同一案件・同一月の二重登録防止）

## 備考

- PoC 段階では複雑性を抑えるため、工数はタスク単位ではなく案件単位・月次で管理する設計とした
- 予算管理（project_budgets）との整合性を考慮し、人月単位での管理としている
- 将来的にはユーザー別・タスク別に拡張可能な構造を想定している
