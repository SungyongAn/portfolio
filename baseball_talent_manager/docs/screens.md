# 画面一覧

## 画面一覧サマリ（画面数・遷移の概要）
- 画面数：14
- 簡易画面の概要
src/
├── components/
│　  └── AppHeader.vue
└── views/
　├── LoginView.vue
　├── club_member/
　│　　├── DashboardView.vue
　│　　├── MeasurementResultReview.vue
　│　　└── MeasurementResultList.vue
　├── manager/
　│　　├── DashboardView.vue
　│　　├── MeasurementResultSubmit.vue
　│　　└── MeasurementResultRejection.vue
　├── coach/
　│　　├── DashboardView.vue
　│　　├── MeasurementResultReview.vue
　│　　├── MeasurementResultList.vue
　│　　└── ClubMemberManagement.vue
　└── director/
　 　　├── DashboardView.vue
　　　 ├── MeasurementResultList.vue
　　 　└── ClubMemberManagement.vue


## 各画面の詳細
- 画面名：LoginView.vue
- 対象ロール：全ロール
- 主な表示項目
　・タイトル
　・メールアドレス入力欄
　・パスワード入力欄
　・ログインボタン
- 主な入力項目
　・メールアドレス
　・パスワード
- 遷移先
　・部員：club_member/DashboardView.vue
　・マネージャー：manager/DashboardView.vue
　・コーチ：coach/DashboardView.vue
　・監督：director/DashboardView.vue


- 画面名：club_member/DashboardView.vue
- 対象ロール：部員
- 主な表示項目
　・測定結果の確認/承認
　・測定結果の閲覧
- 主な入力項目：なし
- 遷移先
　・測定結果の確認/承認：MeasurementResultReview.vue
　・測定結果の閲覧：MeasurementResultList.vue

- 画面名：manager/DashboardView.vue
- 対象ロール：マネージャー
- 主な表示項目
　・測定結果の入力/承認依頼
　・否認の確認/修正
- 主な入力項目：なし
- 遷移先
　・測定結果の入力/承認依頼MeasurementResultSubmit.vue
　・否認の確認/修正：MeasurementResultRejection.vue

- 画面名：coach/DashboardView.vue
- 対象ロール：コーチ
- 主な表示項目
　・測定結果の承認
　・測定結果の閲覧
　・部員の管理画面
- 主な入力項目：なし
- 遷移先
　・測定結果の確認/承認：MeasurementResultReview.vue
　・測定結果の閲覧：MeasurementResultList.vue
　・部員の管理画面：ClubMemberManagement.vue

- 画面名：director/DashboardView.vue
- 対象ロール：監督
- 主な表示項目
　・測定結果の閲覧
　・部員の管理画面
- 主な入力項目：なし
- 遷移先
　・測定結果の閲覧：MeasurementResultList.vue
　・部員の管理画面：ClubMemberManagement.vue


- 画面名
- 対象ロール
- 主な表示項目
- 主な入力項目
- 遷移先

- 画面名
- 対象ロール
- 主な表示項目
- 主な入力項目
- 遷移先

- 画面名
- 対象ロール
- 主な表示項目
- 主な入力項目
- 遷移先
