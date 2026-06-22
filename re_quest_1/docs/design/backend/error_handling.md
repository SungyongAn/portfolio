# error_handling.md

# 例外処理設計

## 1. 概要

本ドキュメントは、`re_quest1` における例外処理およびエラーレスポンス方針を定義する。

第1段階では、既存 `quest_1` で実装した Exception Handler の考え方を ASP.NET Core へ移植する。

---

# 2. 目的

例外処理の目的は以下とする。

- エラーレスポンス形式の統一
- 予期しないエラーの隠蔽
- デバッグ容易性向上
- フロントエンド実装の簡略化
- ログ出力の一元化

---

# 3. 基本方針

## 方針

- Controllerでは例外を捕捉しない
- Serviceで業務例外を発生させる
- Middlewareで共通処理する
- エラーレスポンス形式を統一する

---

# 4. 例外処理フロー

```text
Request
 ↓

Controller
 ↓

Service
 ↓

Exception発生
 ↓

ExceptionMiddleware
 ↓

Response生成
```

---

# 5. エラーレスポンス形式

全エラーを統一形式で返却する。

---

## 基本形式

```json
{
  "detail": "Error Message"
}
```

---

# 6. NotFoundException

## 用途

対象データが存在しない場合。

---

## 例

```text
案件が存在しない
タスクが存在しない
通知が存在しない
```

---

## Response

```json
{
  "detail": "Project not found"
}
```

---

## Status

```text
404 Not Found
```

---

# 7. ForbiddenException

## 用途

権限不足。

---

## 例

```text
他部門案件参照
他人タスク更新
他人通知参照
```

---

## Response

```json
{
  "detail": "Forbidden"
}
```

---

## Status

```text
403 Forbidden
```

---

# 8. UnauthorizedException

## 用途

認証失敗。

---

## 例

```text
JWT無効
JWT期限切れ
ログイン失敗
```

---

## Response

```json
{
  "detail": "Unauthorized"
}
```

---

## Status

```text
401 Unauthorized
```

---

# 9. ValidationException

## 用途

入力値エラー。

---

## 例

```text
progress > 100
budget_amount < 0
name空文字
```

---

## Response

```json
{
  "detail": "Validation Error"
}
```

---

## Status

```text
422 Validation Error
```

---

# 10. BusinessException

## 用途

業務ルール違反。

---

## 例

```text
承認済み案件を再承認
完了案件を着手
却下案件を完了
```

---

## Response

```json
{
  "detail": "Business Rule Error"
}
```

---

## Status

```text
400 Bad Request
```

---

# 11. SystemException

## 用途

予期しないエラー。

---

## 例

```text
DB接続失敗
NullReferenceException
設定不備
```

---

## Response

```json
{
  "detail": "Internal Server Error"
}
```

---

## Status

```text
500 Internal Server Error
```

---

# 12. ExceptionMiddleware

## 役割

例外を共通処理する。

---

## 責務

```text
例外捕捉
ログ出力
HTTPステータス変換
レスポンス生成
```

---

## 想定ファイル

```text
Middleware/
└─ ExceptionMiddleware.cs
```

---

# 13. ログ出力方針

エラー発生時はログ出力する。

---

## 出力対象

```text
例外種別
URL
ユーザーID
StackTrace
```

---

## 出力しないもの

```text
パスワード
JWT本体
機密情報
```

---

# 14. 認可エラー処理

PermissionServiceで権限違反を検出した場合。

---

## 発生例外

```text
ForbiddenException
```

---

## Response

```json
{
  "detail": "Forbidden"
}
```

---

# 15. Validationエラー処理

DTO Validation失敗時。

---

## 発生例外

```text
ValidationException
```

---

## Response

```json
{
  "detail": "Validation Error"
}
```

---

# 16. フロントエンド連携

React側ではHTTPステータスごとに処理を分ける。

---

## 401

```text
ログイン画面へ遷移
```

---

## 403

```text
権限不足メッセージ表示
```

---

## 404

```text
対象データなし表示
```

---

## 422

```text
入力エラー表示
```

---

## 500

```text
システムエラー表示
```

---

# 17. FastAPI版との対応

| FastAPI               | ASP.NET Core        |
| --------------------- | ------------------- |
| exception_handlers.py | ExceptionMiddleware |
| HTTPException         | CustomException     |
| ValidationError       | ValidationException |

---

# 18. 第1段階方針

既存PoCの例外処理方針を維持する。

変更しない内容

- エラーレスポンス形式
- HTTPステータス
- PermissionService連携
- Validation連携

---

# 19. 今後の改善候補

移植完了後に検討する。

- ProblemDetails対応
- RFC7807準拠
- OpenTelemetry連携
- Serilog連携
- エラーコード管理
- 多言語メッセージ対応

---

# 20. まとめ

例外処理は ExceptionMiddleware に集約する。

第1段階では既存PoCのエラーハンドリング方針を維持し、統一されたエラーレスポンスを返却する。
