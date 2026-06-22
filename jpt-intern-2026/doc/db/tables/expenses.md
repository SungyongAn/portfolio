# expenses（直接経費）

## カラム

| カラム名     | 型                                                | NULL | デフォルト                  | 説明                       |
| ------------ | ------------------------------------------------- | ---- | --------------------------- | -------------------------- |
| id           | INT                                               | NO   | AUTO_INCREMENT              | 経費ID                     |
| project_id   | INT                                               | NO   | -                           | 案件ID                     |
| expense_type | ENUM('OUTSOURCING','LICENSE','EQUIPMENT','OTHER') | NO   | -                           | 経費分類（システム定義値） |
| amount       | INT                                               | NO   | -                           | 金額（円）                 |
| description  | TEXT                                              | YES  | NULL                        | 内容説明                   |
| expense_date | DATE                                              | NO   | -                           | 発生日                     |
| created_at   | DATETIME                                          | NO   | CURRENT_TIMESTAMP           | 作成日時                   |
| updated_at   | DATETIME                                          | NO   | CURRENT_TIMESTAMP ON UPDATE | 更新日時                   |

## インデックス

```sql
PRIMARY KEY (id)
INDEX idx_expenses_project_id (project_id)
INDEX idx_expenses_expense_date (expense_date)
INDEX idx_expenses_project_date (project_id, expense_date)
```

## 制約

```sql
FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
CHECK (amount >= 0)
```

## 経費種別定義

| 値          | 表示名       |
| ----------- | ------------ |
| OUTSOURCING | 外注費       |
| LICENSE     | ライセンス費 |
| EQUIPMENT   | 機器・備品   |
| OTHER       | その他       |

## 備考

- expense_type は ENUM で管理することで表記ゆれを防止する
- 種別の追加が必要になった場合は課題2での対応とする
