# notifications（通知）

## カラム

| カラム名   | 型           | NULL | デフォルト        | 説明           |
| ---------- | ------------ | ---- | ----------------- | -------------- |
| id         | INT          | NO   | AUTO_INCREMENT    | 通知ID         |
| user_id    | INT          | NO   | -                 | 受信ユーザーID |
| project_id | INT          | YES  | NULL              | 関連案件ID     |
| title      | VARCHAR(200) | NO   | -                 | 通知タイトル   |
| message    | TEXT         | NO   | -                 | 通知内容       |
| is_read    | BOOLEAN      | NO   | FALSE             | 既読フラグ     |
| created_at | DATETIME     | NO   | CURRENT_TIMESTAMP | 作成日時       |

## インデックス

```sql
PRIMARY KEY (id)
INDEX idx_notifications_user_id (user_id)
INDEX idx_notifications_user_read_created (user_id, is_read, created_at)
INDEX idx_notifications_project_id (project_id)
```

## 制約

```sql
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
```

## 備考

- updated_at は持たない（通知は作成後に内容を変更しない設計）
- 既読管理は is_read フラグのみで行う
- WebSocket によるリアルタイムプッシュ通知に対応
