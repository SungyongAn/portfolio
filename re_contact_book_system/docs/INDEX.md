# 連絡帳管理システム ドキュメント一覧

このディレクトリには、連絡帳管理システムの設計・仕様・更新履歴に関するドキュメントを用途別に整理しています。

> **初めて本プロジェクトを読む方は、README.md → CHANGELOG.md → 設計ドキュメント（design配下）の順で読むことをおすすめします。**

---

## 📘 基本情報
- ../README.md  
  プロジェクト概要、技術スタック、環境構築、起動方法

---

## 🔄 更新履歴

### 全体
- ../CHANGELOG.md  
  プロジェクト全体の変更概要（サマリ）

### コンポーネント別詳細
- changelog/CHANGELOG.backend.md  
  バックエンドの変更履歴
- changelog/CHANGELOG.frontend.md  
  フロントエンドの変更履歴
- changelog/CHANGELOG.database.md  
  データベース設計・マイグレーションの変更履歴

※ 過去の履歴や統合前の変更履歴は `archive/` に保存しています。

---

## 🧱 設計ドキュメント

### 認証・認可
- design/auth-design.md  
  認証方式（JWT・トークン管理）およびセキュリティ設計

### ログイン・レスポンス設計
- design/login-response-design.md  
  ログインAPIおよびレスポンス構造の設計方針

### 教師割当・権限設計
- design/teacher-assignment-design.md  
  担任・副担任・学年主任・教科担当などの割当設計

### データベース設計
- er_diagram.md  
  ER図（テーブル構成・リレーション）
- validation.md  
  バリデーション方針・制約設計

---

## 🛠 開発・運用補助
- ../scripts/create_journal_via_api.py  
  API 経由で日誌エントリを作成する補助スクリプト

---

## 📦 その他
- archive/  
  過去の CHANGELOG や設計資料（参照用・現行仕様では使用しない）
