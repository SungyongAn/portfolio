# トークン設計

| 種別 | 保管場所 | 有効期限 | 用途 |
|------|---------|---------|------|
| Access Token | フロントエンド メモリ（Piniaストア） | 15分 | API認証 |
| Refresh Token | HttpOnly Cookie | 7日 | Access Token更新 |

### Access Tokenをメモリ管理する理由
- XSSで窃取されるリスクを避ける
- リロードで消えるがRefresh Tokenで再取得可能

### Refresh TokenをHttpOnly Cookieで管理する理由
- `HttpOnly` → JSからアクセス不可
- `Secure`（HTTPS限定）・`SameSite=Strict` → CSRF対策

### 環境別Cookie設定

| 属性 | 開発環境 | 本番環境（Oracle Cloud） |
|------|---------|----------------------|
| `HttpOnly` | ✅ | ✅ |
| `Secure` | ❌ | ✅ |
| `SameSite` | `Lax` | `Strict` |

> 本番デプロイ時は`.env`で `COOKIE_SECURE=true`、`COOKIE_SAMESITE=Strict` に設定

### JWTペイロード

```json
{
  "sub": "user_id",
  "role": "student | librarian | admin",
  "is_committee": false,
  "school_id": 1,
  "exp": 1234567890
}
```

- is_committeeはrole: "student"の場合のみ有効
- nameはJWTに含めず、ログインレスポンスやGET /api/auth/meで取得
