# 画面設計

## 画面一覧

| 画面ID | 画面名 | ロール | 課題区分 | 詳細ファイル |
|--------|--------|--------|---------|------------|
| SCR-01 | ログイン | 全員 | 課題1 | SCR-01-login.md |
| SCR-02 | ダッシュボード（生徒・図書委員） | student / committee | 課題1 | SCR-02-dashboard-student.md |
| SCR-03 | ダッシュボード（司書） | librarian | 課題1 | SCR-03_librarian_dashboard.md |
| SCR-04 | ダッシュボード（管理者） | admin | 課題1 | SCR-04_admin_dashboard.md |
| SCR-05 | 資料検索・一覧 | 全員 | 課題1 | SCR-05_search_list.md |
| SCR-06 | 資料詳細 | 全員 | 課題1 | SCR-06_book_detail.md |
| SCR-07 | マイページ（貸出・予約一覧） | student / committee | 課題1 | SCR-07_mypage.md |
| SCR-08 | パスワード変更 | 全員 | 課題1 | SCR-08_password_change.md |
| SCR-09 | 資料管理（司書） | librarian | 課題1 | SCR-09_book_management.md |
| SCR-10 | 送付リスト・受取登録（司書） | librarian | 課題1 | SCR-10_transfer_receive.md |
| SCR-11 | 生徒アカウント管理 | admin | 課題1 | SCR-11_student_account_management.md |
| SCR-12 | パスワードリセット申請 | 全員（未ログイン） | 課題1 | SCR-12_password_reset_request.md |
| SCR-13 | パスワードリセット実行 | 全員（未ログイン） | 課題1 | SCR-13_password_reset_execute.md |
| SCR-14 | 貸出管理（図書委員） | committee | 課題1 | SCR-14_loan_management_committee.md |
| SCR-15 | 貸出管理（司書） | librarian | 課題1 | SCR-15_loan_management_librarian.md |
| SCR-16 | 貸出処理 | student / committee / librarian | 課題1 | SCR-16_loan_checkout.md |
| SCR-17 | 返却処理 | student / committee / librarian | 課題1 | SCR-17_return_process.md |

---

## 貸出ルール

| ルール | 内容 |
|--------|------|
| 貸出上限 | 1人あたり同時5冊まで（図書館間貸出を含む） |
| 延滞制限 | 延滞中（返却期限超過）の資料がある場合、新規貸出・予約不可 |
| 制限の適用 | 代理操作時も同様に適用。フロント表示制御＋バックエンドAPI検証の両方で担保 |

---

## 画面遷移図

```
[SCR-12 パスワードリセット申請] ←─ [SCR-01 ログイン] ──→ [SCR-13 パスワードリセット実行]
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              ↓                           ↓                           ↓
 [SCR-02 生徒・図書委員ダッシュボード]   [SCR-03 司書ダッシュボード]   [SCR-04 管理者ダッシュボード]
       │                                  │                           │
       ├──→ [SCR-05 資料検索]            ├──→ [SCR-05 資料検索]     ├──→ [SCR-11 アカウント管理]
       │         └──→ [SCR-06 資料詳細]  │        └──→ [SCR-06]     └──→ [SCR-08 パスワード変更]
       ├──→ [SCR-16 貸出処理]            ├──→ [SCR-16 貸出処理]
       ├──→ [SCR-17 返却処理]            ├──→ [SCR-17 返却処理]
       ├──→ [SCR-07 マイページ]          ├──→ [SCR-09 資料管理]
       ├──→ [SCR-14 貸出管理]※委員のみ  ├──→ [SCR-10 送付リスト・受取登録]
       └──→ [SCR-08 パスワード変更]      ├──→ [SCR-15 貸出管理]
                                         └──→ [SCR-08 パスワード変更]
```

> SCR-05/06は全ロールからアクセス可能（遷移図では代表的な経路のみ記載）