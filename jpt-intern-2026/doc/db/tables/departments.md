# departments（部門）

## カラム

| カラム名 | 型           | NULL | デフォルト     | 説明             |
| -------- | ------------ | ---- | -------------- | ---------------- |
| id       | INT          | NO   | AUTO_INCREMENT | 部門ID           |
| name     | VARCHAR(100) | NO   | -              | 部門名（UNIQUE） |

## インデックス

```sql
PRIMARY KEY (id)
UNIQUE INDEX uq_departments_name (name)
```
