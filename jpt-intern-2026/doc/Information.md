# Information

## デプロイ先URL

http://158.101.148.143

---

## 動作確認用テストアカウント一覧

| ユーザー名 | メールアドレス                 | パスワード | ロール                     | 部門                       |
| ---------- | ------------------------------ | ---------- | -------------------------- | -------------------------- |
| 亀田 大輔  | kameda@nextflow.example.com    | password   | TASK_MEMBER（担当者）      | プロダクト開発部           |
| 斉藤 彩香  | saito@nextflow.example.com     | password   | TASK_MEMBER（担当者）      | カスタマーソリューション部 |
| 林 直樹    | hayashi@nextflow.example.com   | password   | TASK_MEMBER（担当者）      | プロダクト開発部           |
| 中村 葵    | nakamura@nextflow.example.com  | password   | TASK_MEMBER（担当者）      | カスタマーソリューション部 |
| 田中 翔太  | tanaka@nextflow.example.com    | password   | APPLICANT（申請者）        | プロダクト開発部           |
| 佐藤 美咲  | sato@nextflow.example.com      | password   | APPLICANT（申請者）        | カスタマーソリューション部 |
| 鈴木 健一  | suzuki@nextflow.example.com    | password   | DEPT_MANAGER（部門管理者） | プロダクト開発部           |
| 山田 誠    | yamada@nextflow.example.com    | password   | DEPT_MANAGER（部門管理者） | カスタマーソリューション部 |
| 高橋 裕子  | takahashi@nextflow.example.com | password   | HQ_MANAGER（本部管理者）   | 開発本部                   |

---

## 推奨ブラウザ

- Google Chrome（推奨）
- Microsoft Edge

---

## 動作確認手順

### 1. アプリへアクセス

ブラウザで以下にアクセスしてください。

```txt
http://158.101.148.143
```

---

### 2. 任意のテストアカウントでログイン

上記一覧の任意アカウントをご利用ください。

---

### 3. 初回確認おすすめ順

1. `HQ_MANAGER` でログイン
2. ダッシュボード確認
3. 通知機能確認
4. 案件詳細・ガントチャート確認
5. 予算管理画面確認

---

### 4. 推奨確認シナリオ

#### APPLICANT（申請者）

- 新規案件申請
- 自案件一覧確認
- タスク登録・更新
- 工数実績 / 経費登録
- ガントチャート確認
  - 担当者フィルター
  - 日 / 週 / 月切替
  - 本日ライン
  - 📍 今日へ移動
- KPIカード選択による案件一覧切替確認

---

#### TASK_MEMBER（担当者）

- 自部門案件一覧確認
- 割当タスク更新
- 今日の対応タスク確認
- 担当タスク一覧フィルター確認
- KPIカード選択による案件一覧切替確認

---

#### DEPT_MANAGER（部門管理者）

- 自部門案件確認
- 一次承認
- メンバータスク状況確認
- アラートダッシュボード確認
- ダッシュボードカード選択による案件一覧切替確認

---

#### HQ_MANAGER（本部管理者）

- 全案件確認
- 最終承認
- 全部門予算状況確認
- アラートダッシュボード確認
- ダッシュボードカード選択による案件一覧切替確認

---

### 通知機能（全ロール共通）

- 未読通知バッジ確認
- 通知一覧（PC：Popover / スマホ：Drawer）確認
- 通知詳細Dialog確認
- WebSocketによるリアルタイム通知
- seed品質監査を通じて、案件責任者表示や却下理由可視化など、実務利用を意識した改善提案を整理済み

---

### モバイル対応について

本PoCではPCブラウザでの業務利用を優先して設計し、
レスポンシブ対応も実装しています。

スマホUIについては実装済みですが、
実機による最終動作確認は今後の確認項目です。

- Headerメニュー
- Drawerメニュー
- 通知一覧（Drawer）
- ダッシュボード表示
- 案件詳細表示

※ 実装は完了していますが、実機による最終動作確認は今後の確認項目です。  
※ ブラウザのレスポンシブモードで確認可能です。

---

## 備考

- 全アカウントのパスワードは `password` です
- `seed.py` 実行時点の日付を基準に、今日の対応タスク・期限超過タスク・危険案件が再現されます
- 限られた開発期間のため、優先度の高い PC動作確認を先行実施しています
- デプロイ環境：Oracle Cloud Infrastructure（Always Free）
- OS：Ubuntu 24.04 LTS
- 起動方式：Docker Compose
- 認証方式：JWT Authentication
