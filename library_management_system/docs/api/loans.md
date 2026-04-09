# 貸出 API

ベースパス：`/api/loans`

| メソッド | パス | 概要 | 権限 |
|---------|------|------|------|
| POST | `/loan-by-barcode` | バーコードで貸出処理 | student, committee, librarian |
| PATCH | `/return-by-barcode` | バーコードで返却処理 | student, committee, librarian |
| GET | `/my` | 自分の貸出一覧 | student, committee |

### POST /loan-by-barcode
バーコードから資料を特定し、貸出可否チェックのうえ貸出を確定する。

**Request**
```
barcode, user_id（committee・librarian が代理操作する場合のみ）
```
**Response**
```
loan_id, book_id, title, user_id, loaned_at, due_at
```
**エラー（400）**
```
資料が存在しない / 貸出上限超過（同時5冊）/ 延滞中資料あり / 他に予約者がいる / 貸出不可ステータス
```

### PATCH /return-by-barcode
バーコードから現在の貸出記録を特定し、返却処理を確定する。

**Request**
```
barcode, user_id（committee・librarian が代理操作する場合のみ）
```
**Response**
```
loan_id, book_id, title, returned_at, next_reservation_user_name（次の予約者がいる場合）
```
**エラー（400）**
```
資料が存在しない / 貸出中の記録が存在しない
```

---

## 関連ユースケース

- UC-11 資料貸出
- UC-12 資料返却
- UC-13 自分の貸出一覧確認