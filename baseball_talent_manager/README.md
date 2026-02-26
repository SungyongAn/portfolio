# Baseball Talent Manager（PoC）

## 概要
本リポジトリは、部活動における測定結果管理業務を対象とした  
PoC（Proof of Concept）プロジェクトです。

本PoCでは以下を検証対象とします。

- ロール別の業務フローをシステム化できるか
- 測定結果の入力・承認・閲覧フローの実現可能性
- Webアプリとしての基本構成の成立性

※本プロジェクトは本番運用を目的としたものではなく、
PoCとして最小構成で検証を行うものです。

---

## 開発状況

現在は **PoC設計フェーズ終盤** です。  
画面設計を進めながら、フロントエンド雛形構築を開始しています。

### 完了
- 課題精査
- ユースケース整理（docs/usecase.md）
- PoC機能決定（docs/functions.md）
- 画面設計（docs/screens.md）
- フロントエンド環境構築（Vite）
- 基本アプリ構成作成（App.vue / main.js）
- 参考資料の整理

### 進行中
- API設計（docs/api.md / docs/auth_design.md / docs/role_matrix.md）

### 次の予定
- DB設計（docs/er.md）
- モックUI作成

---

## 設計ドキュメント

設計関連ドキュメントは docs フォルダに格納しています。

- ユースケース整理  
  `docs/usecase.md`

- PoC機能一覧  
  `docs/functions.md`

- 画面設計  
  `docs/screens.md`（作成中）

---

## 参考資料

課題資料・検討用ファイルは以下に格納しています。
`docs/reference_materials/`

## ディレクトリ構成（主要部分）

backend/ バックエンド実装予定
```
docs/
├─ usecase.md ユースケース整理
├─ functions.md PoC機能一覧
├─ screens.md 画面設計（作成中）
└─ reference_materials/
　　├─ 課題PDF
　　└─ 記録ファイル

frontend/
├─ src/
├─ App.vue
├─ main.js
└─ vite.config.js
```

## 技術スタック（予定）

### Frontend
- Vue 3
- Vite
- Vue Router（予定）
- Pinia（予定）

### Backend
- FastAPI（予定）

### Database
- PostgreSQL（予定）

### 認証
- メール＋パスワード認証
- パスワードハッシュ化（argon2想定）
- JWTベース認証（予定）

### 開発環境
- Docker / docker-compose（予定）

---

## 起動方法（フロントエンド）

```bash
cd frontend
npm install
npm run dev
```

## 備考

本リポジトリは段階的に設計→プロトタイプ実装→改善の順で進めます。
