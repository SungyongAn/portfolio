# 貸出状況管理 API

ベースパス：`/api/loans/management`

| メソッド | パス | 概要 | 権限 |
|---------|------|------|------|
| GET | `/` | 自校生徒の貸出・予約・延滞状況一覧 | committee, librarian |
| GET | `/overdue` | 延滞中資料一覧 | librarian |
| GET | `/overdue/csv` | 延滞一覧CSV出力 | librarian |

### GET /
**Query**
```
name, grade, class_name, has_overdue（延滞フィルター）, page, per_page
```
**Response**
```
students: [{ user_id, name, grade, class_name, loan_count, has_overdue, loans: [...], reservations: [...] }], total, page, per_page
```

---

## 関連ユースケース

- UC-14 貸出状況一覧確認
- UC-15 延滞一覧確認
- UC-16 延滞一覧CSV出力