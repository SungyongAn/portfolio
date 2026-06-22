# 画面遷移

## 概要

本ドキュメントでは、各画面間の遷移関係と業務フロー上の導線を定義する。

---

## 全体遷移図

```text
ログイン画面（S-AUTH-01）
  ↓
ダッシュボード（S-CMN-01）
  ├─ 案件申請Drawer（S-APP-02）※APPLICANTのみ・Drawer表示
  ├─ 案件一覧画面（S-APP-01）
  │    ├─ 案件申請画面（S-APP-02）※APPLICANTのみ・/projects/new
  │    └─ 案件詳細画面（S-APP-03）
  │         ├─ 承認・却下画面（S-APR-01）※DEPT_MANAGER / HQ_MANAGERのみ
  │         ├─ タスク登録画面（S-TSK-01）※APPLICANTのみ・承認済み案件のみ
  │         ├─ タスク更新Dialog ※インライン表示（画面遷移なし）
  │         └─ 予算管理画面（S-BDG-01）
  │              ├─ 工数実績入力画面（S-BDG-02）※APPLICANTのみ
  │              └─ 直接経費入力画面（S-BDG-03）※APPLICANTのみ
  ├─ 予算管理一覧画面（S-BDG-04）※DEPT_MANAGER / HQ_MANAGERのみ
  ├─ メンバータスク状況画面（S-MBR-01）※DEPT_MANAGERのみ
  └─ 通知一覧画面（S-NTF-01）
```
