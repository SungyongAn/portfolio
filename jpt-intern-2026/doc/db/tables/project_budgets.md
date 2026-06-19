# project_budgets（案件予算管理）

## カラム

| カラム名       | 型       | NULL | デフォルト                  | 説明                      |
| -------------- | -------- | ---- | --------------------------- | ------------------------- |
| id             | INT      | NO   | AUTO_INCREMENT              | 予算ID                    |
| project_id     | INT      | NO   | -                           | 案件ID（UNIQUE・1:1保証） |
| budget_amount  | INT      | NO   | -                           | 予算額（円）              |
| unit_price     | INT      | YES  | NULL                        | 人月単価（円）            |
| planned_months | INT      | YES  | NULL                        | 計画工数（人月）          |
| actual_amount  | INT      | NO   | 0                           | 実績額（円）              |
| created_at     | DATETIME | NO   | CURRENT_TIMESTAMP           | 作成日時                  |
| updated_at     | DATETIME | NO   | CURRENT_TIMESTAMP ON UPDATE | 更新日時                  |

## インデックス

```sql
PRIMARY KEY (id)
UNIQUE INDEX uq_project_budgets_project_id (project_id)
```

## 制約

```sql
FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
CHECK (budget_amount >= 0)
CHECK (actual_amount >= 0)
```

## 補足

- 実績額（actual_amount）は worklogs の工数合計 × unit_price + expenses の合計で自動計算し更新する
- 消費率はアプリケーション側で `actual_amount / budget_amount * 100` として算出する
- unit_price は案件確定時点の固定値として保持し、後から変更されても予算には影響させない
