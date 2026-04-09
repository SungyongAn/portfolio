# 予約 API

ベースパス：`/api/reservations`

| メソッド | パス | 概要 | 権限 |
|---------|------|------|------|
| GET | `/my` | 自分の予約一覧 | student, committee |
| POST | `/` | 予約・順番待ち登録 | student, committee, librarian |
| DELETE | `/{reservation_id}` | 自校資料の予約キャンセル | student, committee, librarian |

### DELETE /{reservation_id}
- キャンセル可能ステータス：`waiting`・`ready`
- `completed`・`cancelled`の場合は400エラーを返す

### POST /
**Request**
```
book_id, user_id（committee・librarian が代理操作する場合のみ）
```
**Response**
```
reservation_id, book_id, queue_order, status
```
**エラー（400）**
```
貸出上限超過（同時5冊）/ 延滞中資料あり / 重複予約
```

---

## 関連ユースケース

- UC-07 資料予約（自校蔵書）
- UC-08 順番待ち（貸出中資料）
- UC-09 予約キャンセル
- UC-10 自分の予約一覧確認 