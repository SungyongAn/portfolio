# projects（案件）

## カラム

| カラム名           | 型                                                                                        | NULL | デフォルト                  | 説明             |
| ------------------ | ----------------------------------------------------------------------------------------- | ---- | --------------------------- | ---------------- |
| id                 | INT                                                                                       | NO   | AUTO_INCREMENT              | 案件ID           |
| applicant_id       | INT                                                                                       | NO   | -                           | 申請者ID         |
| department_id      | INT                                                                                       | NO   | -                           | 担当部門ID       |
| name               | VARCHAR(200)                                                                              | NO   | -                           | 案件名           |
| description        | TEXT                                                                                      | YES  | NULL                        | 概要             |
| status             | ENUM('DRAFT','PENDING_DEPT','PENDING_HQ','APPROVED','IN_PROGRESS','COMPLETED','REJECTED') | NO   | 'DRAFT'                     | ステータス       |
| development_method | ENUM('WATERFALL','AGILE')                                                                 | YES  | NULL                        | 開発手法         |
| budget_amount      | INT                                                                                       | YES  | NULL                        | 概算予算（円）   |
| planned_months     | INT                                                                                       | YES  | NULL                        | 概算工数（人月） |
| start_date         | DATETIME                                                                                  | YES  | NULL                        | 開始日           |
| end_date           | DATETIME                                                                                  | YES  | NULL                        | 完了予定日       |
| reject_reason      | TEXT                                                                                      | YES  | NULL                        | 却下理由         |
| created_at         | DATETIME                                                                                  | NO   | CURRENT_TIMESTAMP           | 作成日時         |
| updated_at         | DATETIME                                                                                  | NO   | CURRENT_TIMESTAMP ON UPDATE | 更新日時         |

## インデックス

```sql
PRIMARY KEY (id)
INDEX idx_projects_applicant_id (applicant_id)
INDEX idx_projects_department_id (department_id)
INDEX idx_projects_status (status)
INDEX idx_projects_applicant_status (applicant_id, status)
INDEX idx_projects_department_status (department_id, status)
INDEX idx_projects_created_at (created_at)
```

## 制約

```sql
FOREIGN KEY (applicant_id) REFERENCES users(id) ON DELETE RESTRICT
FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT
```

## 備考

- ステータスについて
  - 申請時のデフォルトは `DRAFT`（下書き保存から申請への流れを想定）
  - ステータス遷移の詳細は `status_design.md` を参照

- development_method について
  - 現行 PoC ではウォーターフォール型案件管理のみ対象
  - 将来的なアジャイル案件対応を考慮し DB 上はカラムを保持している

- 予算・工数について
  - `budget_amount` は申請時の概算予算（円単位）
  - `planned_months` は概算工数（人月単位）
  - 承認後の正式予算・実績は `project_budgets` テーブルで管理

- 却下理由について
  - `reject_reason` は却下時のみ設定（500字以内）

- ページネーション対応について
  - 案件一覧取得時は `created_at` の降順でソートし `OFFSET/LIMIT` で取得
  - キーワード検索は `name` カラムの部分一致で実施
