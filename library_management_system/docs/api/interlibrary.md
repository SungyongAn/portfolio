# 図書館間貸出 API

ベースパス：`/api/inter-library`

| メソッド | パス | 概要 | 権限 |
|---------|------|------|------|
| POST | `/` | 他校資料予約 | student, committee, librarian |
| DELETE | `/{request_id}` | 図書館間貸出予約キャンセル | student, committee, librarian |
| GET | `/outgoing` | 送付リスト取得（今週分） | librarian |
| PATCH | `/{request_id}/ship` | 発送登録 | librarian |
| PATCH | `/{request_id}/receive` | 受取登録 | librarian |
| GET | `/my` | 自分の図書館間貸出一覧 | student, committee |

## ステータス定義

- pending：申請中
- confirmed：確定（締め処理後）
- shipped：発送済み
- received：受取済み（取り置き）
- on_loan：貸出中
- returned：返却済み
- cancelled：キャンセル

### POST /
**Request**
```
book_id, user_id（committee・librarian が代理操作する場合のみ）
```
**Response**
```
request_id, book_id, from_school_id, to_school_id, status, deadline
```

### DELETE /{request_id}
- キャンセル可能ステータス：`pending`・`confirmed`
- それ以外は400エラー

### PATCH /{request_id}/ship
**Request**
```
shipped_at（省略時はサーバー時刻）
```
**Response**
```
request_id, status, shipped_at
```

### GET /outgoing
**Query**
```
deadline（指定なしで直近の金曜日）
```
**Response**
```
requests: [{ request_id, book_id, title, barcode, to_school_name, requested_user_name }]
```

### PATCH /{request_id}/receive
- 受取登録後、予約者にメール通知を送信する

---

## 関連ユースケース

- UC-17 図書館間貸出申請
- UC-18 図書館間貸出キャンセル
- UC-19 自分の図書館間貸出一覧確認
- UC-20 発送登録
- UC-21 受取登録
- UC-22 送付リスト確認