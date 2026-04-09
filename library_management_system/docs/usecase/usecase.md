# ユースケース定義

## 登場人物（ロール）と権限概要

| ロール | 値 | 説明 |
|--------|-----|------|
| 生徒 | `student` | 各校に在籍する生徒。自身の資料の検索・予約・貸出・返却・パスワード変更を行う |
| 図書委員 | `student`（`is_committee: true`） | 生徒の権限に加え、他生徒の資料の検索・予約・貸出・返却を代理で行う |
| 司書 | `librarian` | 各校の図書館担当者。資料管理・図書館間貸出の発送受取、他生徒の代理操作を行う |
| 管理者 | `admin` | システム全体の管理者。生徒アカウントの登録・削除を行う |

> **図書委員について**：ロールは`student`のまま`is_committee`フラグで権限を制御する（案B）。将来的な権限テーブル方式への移行を見据えたシンプルな設計。

---

## ユースケース一覧

| ID | 名称 | ファイル | 画面 |
|----|------|---------|------|
| UC-01 | ログイン | auth.md | SCR-01 |
| UC-02 | パスワードリセット申請 | auth.md | SCR-12 |
| UC-03 | パスワードリセット実行 | auth.md | SCR-13 |
| UC-04 | パスワード変更 | auth.md | SCR-08 |
| UC-05 | 資料検索 | search.md | SCR-05 |
| UC-06 | 資料詳細取得 | search.md | SCR-06 |
| UC-07 | 資料予約（自校蔵書） | reservation.md | SCR-06 |
| UC-08 | 順番待ち（貸出中資料） | reservation.md | SCR-06 |
| UC-09 | 予約キャンセル | reservation.md | SCR-07 |
| UC-10 | 自分の予約一覧確認 | reservation.md | SCR-07 |
| UC-11 | 資料貸出 | loan.md | SCR-16 |
| UC-12 | 資料返却 | loan.md | SCR-17 |
| UC-13 | 自分の貸出一覧確認 | loan.md | SCR-07 |
| UC-14 | 貸出状況一覧確認 | loan-management.md | SCR-14 |
| UC-15 | 延滞一覧確認 | loan-management.md | SCR-15 |
| UC-16 | 延滞一覧CSV出力 | loan-management.md | SCR-15 |
| UC-17 | 図書館間貸出予約 | interlibrary.md | SCR-06 |
| UC-18 | 図書館間貸出キャンセル | interlibrary.md | SCR-06 |
| UC-19 | 自分の図書館間貸出一覧確認 | interlibrary.md | SCR-07 |
| UC-20 | 発送登録 | interlibrary.md | SCR-10 |
| UC-21 | 受取登録 | interlibrary.md | SCR-10 |
| UC-22 | 送付リスト確認 | interlibrary.md | SCR-10 |
| UC-23 | 資料追加 | librarian.md | SCR-09 |
| UC-24 | 資料情報更新 | librarian.md | SCR-09 |
| UC-25 | 資料廃棄 | librarian.md | SCR-09 |
| UC-26 | 生徒アカウント登録 | admin.md | SCR-11 |
| UC-27 | 生徒アカウント削除 | admin.md | SCR-11 |
| UC-28 | 生徒一覧取得 | admin.md | SCR-11 |
| UC-29 | 生徒詳細取得 | admin.md | SCR-11 |

---

## 最小限必要な画面一覧

| 画面 | ロール | 対応SCR |
|------|--------|---------|
| ログイン | 全員 | SCR-01 |
| パスワードリセット申請 | 全員（未ログイン） | SCR-12 |
| パスワードリセット実行 | 全員（未ログイン） | SCR-13 |
| ダッシュボード（生徒・図書委員） | student（is_committee含む） | SCR-02 |
| ダッシュボード（司書） | librarian | SCR-03 |
| ダッシュボード（管理者） | admin | SCR-04 |
| 資料検索・一覧 | 全員 | SCR-05 |
| 資料詳細（予約・順番待ち） | 全員 | SCR-06 |
| マイページ（貸出中・予約一覧） | student（is_committee含む） | SCR-07 |
| パスワード変更 | 全員 | SCR-08 |
| 資料管理（追加・廃棄） | librarian | SCR-09 |
| 送付リスト・受取登録 | librarian | SCR-10 |
| 生徒アカウント管理 | admin | SCR-11 |
| 貸出管理 | student（is_committee: true） | SCR-14 |
| 貸出管理 | librarian | SCR-15 |
| 貸出処理 | student / committee / librarian | SCR-16 |
| 返却処理 | student / committee / librarian | SCR-17 |

---

## システム処理
詳細は `system.md` を参照

---

## 関連ドキュメント
- 画面設計：`/screens`
- API設計：`/api/api.md`
- 認証設計：`/auth/auth.md`