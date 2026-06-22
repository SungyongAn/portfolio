# Design Documents

# 設計書一覧

本ディレクトリは、`re_quest1` の設計ドキュメントを管理する。

---

# 設計書構成

```text
docs/design/
│
├─ README.md
│
├─ system_design.md
├─ database_design.md
├─ api_design.md
├─ frontend_design.md
└─ backend_design.md
```

---

# 設計書参照順序

設計書は以下の順序で参照する。

```text
system_design
 ↓

database_design
 ↓

api_design
 ↓

frontend_design
 ↓

backend_design
```

---

# 設計書一覧

## 1. system_design.md

システム全体設計書

### 内容

- システム概要
- システム構成
- 利用者
- 機能構成
- ロール設計
- ステータス設計
- 認証・認可
- アラート設計

### 対象者

- 全開発者

---

## 2. database_design.md

データベース設計書

### 内容

- ER構成
- テーブル設計
- カラム設計
- リレーション
- インデックス
- 制約
- バリデーション方針

### 対象者

- バックエンド開発者
- DB設計担当

---

## 3. api_design.md

API設計書

### 内容

- API一覧
- Request
- Response
- ステータスコード
- 認証
- 認可

### 対象者

- フロントエンド開発者
- バックエンド開発者

---

## 4. frontend_design.md

フロントエンド設計書

### 内容

- React構成
- ルーティング
- 状態管理
- コンポーネント構成
- API通信
- UI方針

### 対象者

- フロントエンド開発者

---

## 5. backend_design.md

バックエンド設計書

### 内容

- ASP.NET Core構成
- Controller設計
- Service設計
- Repository設計
- DTO設計
- Validation設計
- 例外処理設計

### 対象者

- バックエンド開発者

---

# 設計依存関係

## system_design

最上位設計

```text
system_design
 ├─ database_design
 ├─ api_design
 ├─ frontend_design
 └─ backend_design
```

---

## database_design

以下へ影響する

```text
database_design
 ├─ api_design
 └─ backend_design
```

---

## api_design

以下へ影響する

```text
api_design
 ├─ frontend_design
 └─ backend_design
```

---

## frontend_design

以下を参照する

```text
system_design
api_design
```

---

## backend_design

以下を参照する

```text
system_design
database_design
api_design
```

---

# 開発時の確認順序

## 新機能追加時

```text
1. system_design更新
 ↓

2. database_design更新
 ↓

3. api_design更新
 ↓

4. frontend_design更新
 ↓

5. backend_design更新
 ↓

6. 実装
```

---

## API変更時

```text
api_design更新
 ↓

frontend_design確認
 ↓

backend_design確認
 ↓

実装
```

---

## DB変更時

```text
database_design更新
 ↓

api_design更新
 ↓

backend_design更新
 ↓

実装
```

---

# 今後の拡張予定

設計書の肥大化を防ぐため、
必要に応じて以下へ分割する。

```text
docs/design/
│
├─ database/
│
├─ api/
│
├─ frontend/
│
└─ backend/
```

---

# Phase 1

既存PoC移植

対象

- React移植
- ASP.NET Core移植
- MySQL移植

---

# Phase 2

改善

対象

- 認証強化
- UI改善
- テスト強化
- CI/CD
- 運用改善

---

# ドキュメント更新ルール

以下の場合は更新する。

- テーブル追加
- API追加
- 画面追加
- ロール変更
- 権限制御変更
- 設計変更

---

# まとめ

本ディレクトリ内の設計書は、

```text
system_design
 ↓

database_design
 ↓

api_design
 ↓

frontend_design
 ↓

backend_design
```

の順に依存している。

設計変更時は依存関係を考慮して更新すること。
