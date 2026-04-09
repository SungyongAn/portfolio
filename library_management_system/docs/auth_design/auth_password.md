
# パスワード管理

## パスワードハッシュ

- アルゴリズム：Argon2id
- ライブラリ：`argon2-cffi`（Python）

## パスワードリセットトークン管理

| 項目 | 内容 |
|------|------|
| 生成方式 | `secrets.token_urlsafe(32)` |
| 有効期限 | 30分 |
| 使い捨て | 使用後は`used_at`記録し無効化 |
| 送信方式 | URLをメールで送信 |
| 保管場所 | `password_reset_tokens`テーブル |

### パスワードリセットフロー

1. POST /api/auth/password-reset/request → DBにトークン保存、メール送信
2. ユーザーがURLクリック → パスワード入力
3. POST /api/auth/password-reset/execute → トークン有効性チェック
4. 成功 → パスワード更新、used_at記録
5. 無効 → 400エラー

## パスワード変更

- `PATCH /api/auth/password`  
- Request: `current_password, new_password`