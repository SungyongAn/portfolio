# 資料管理 API

ベースパス：`/api/books`

| メソッド | パス | 概要 | 権限 |
|---------|------|------|------|
| GET | `/` | 資料検索・一覧取得 | 全員 |
| POST | `/` | 資料追加 | librarian |
| GET | `/{book_id}` | 資料詳細取得 | 全員 |
| PATCH | `/{book_id}` | 資料情報更新・廃棄 | librarian |

### GET /
**Query**
```
keyword, school_id, ndc, status, isbn, page, per_page
```
**Response**
```
books: [{ id, school_id, school_name, barcode, title, author, isbn, ndc, publisher, published_year, status }], total, page, per_page
```

### GET /{book_id}
**Response**
```
id, school_id, school_name, barcode, title, author, isbn, ndc, publisher, published_year, status,
reservation_count（予約・順番待ち人数）,
current_loan: { user_name, due_at }（貸出中の場合のみ）
```

### POST /
**Request**
```
school_id, barcode, title, author, isbn, ndc, publisher, published_year
```

### PATCH /{book_id}
**Request**
```
status（"disposed"指定で廃棄）, title, author, ndc, publisher, published_year
```

---

## 関連ユースケース

- UC-05 資料検索
- UC-06 資料詳細取得
- UC-23 資料追加
- UC-24 資料情報更新 
- UC-25 資料廃棄