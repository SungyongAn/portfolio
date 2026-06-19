# 画面設計

## 概要
本ドキュメントでは、本システムにおける画面構成・画面遷移・各画面の入出力項目を定義する。

業務要件をもとに、ユーザー操作とシステム挙動が一貫するよう設計している。

---

## スコープ
- 画面一覧
- 画面遷移
- 各画面の表示項目 / 入力項目 / 操作
- ロールごとの表示・操作制御

※ UIデザイン（見た目）は本ドキュメントの対象外

---

## 構成
screens/
├── README.md           ：本ドキュメント
├── screen-list.md      ：画面一覧
├── navigation.md       ：画面遷移
└── screens/            ：各画面の詳細設計
      ├── auth.md             S-AUTH-01：ログイン画面
      ├── dashboard.md        S-CMN-01：ダッシュボード
      ├── project.md          S-APP-01：案件一覧画面
      ├── project_apply.md    S-APP-02：案件申請画面
      ├── project_detail.md   S-APP-03：案件詳細画面
      ├── approval.md         S-APR-01：承認・却下画面
      ├── task.md             S-TSK-01：タスク登録・更新画面
      ├── budget.md           S-BDG-01/02/03：予算管理系画面
      └── notification.md     S-NTF-01：通知一覧画面

---

## 関連ドキュメント
- `../requirements/` ：業務要件
- `../functions.md` ：機能一覧
- `../role_matrix.md` ：権限管理
- `../api_design.md` ：API設計