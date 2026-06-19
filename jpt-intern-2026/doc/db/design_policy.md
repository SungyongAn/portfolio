# 設計方針

- 派生データは保持しない
- 集計はクエリで算出する
- tasksは階層構造を持たないフラット構造とする
- project_budgetsは1:1構成（project_idをPKとする）
- 工数実績はworklogsで案件単位・月次で管理する
- 直接経費はexpensesで案件単位・発生都度で管理する
- 重複入力はユニーク制約で防止する
- 通知はproject or task必須（CHECK制約）
- アクセストークンはメモリで管理・リフレッシュトークンはhttpOnly Cookieで管理する