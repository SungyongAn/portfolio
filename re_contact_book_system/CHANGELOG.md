# Changelog

このファイルはプロジェクト全体の変更履歴管理方針の変更を記録します。
各コンポーネントの詳細な変更履歴は以下を参照してください：

- [Backend](./docs/changelog/CHANGELOG-backend.md)
- [Frontend](./docs/changelog/CHANGELOG-frontend.md)
- [Database](./docs/changelog/CHANGELOG-database.md)

---

## 2026/02/10
### Changed
- 教師の担当情報設計を整理
  - `001_initial_schema.py` を修正

### Fixed
- 管理画面のユーザー一覧ページで、教師・生徒・管理者の役割・学年・クラスが正しく表示されるよう改善
- 代表割当や割当情報が存在しない場合でも、安全に表示されるよう修正し、表示崩れやエラーを防止
- 教師ユーザーの代表割当取得時の `AttributeError` を修正

## 2026/02/09
### Changed
- CHANGELOG の構成を見直し、責務ごとに分割
  - 単一ファイルから Backend / Frontend / Database の3ファイルに分離
  - 各ファイルの配置先: `docs/changelog/`
  - 設計判断・方針は Design ドキュメントへ移動
    - `docs/design/auth-design.md`
    - `docs/design/teacher-assignment-design.md`
    - `docs/design/login-response-design.md`

### Improved
- CHANGELOG の可読性・保守性を向上
  - コンポーネント単位での変更追跡が容易に
  - 各担当者が関連する変更履歴のみを参照可能
  - 設計の変遷と実装の変更を明確に分離

### Migration Guide
- 統合版CHANGELOG（2025/12/20〜2026/02/06）は `docs/archive/CHANGELOG-legacy.md` に移動
- 2026/02/09 以降の変更は各コンポーネント別CHANGELOGに記録

## 2026/02/06
- 教師ユーザーのログインレスポンス設計を整理
- 教師の複数割当に対応した代表割当（primary_assignment）の導入
- 教師割当取得ロジックを service 層に集約  
  （詳細：Backend Changelog）

---

## 2026/02/05
- 管理者向けユーザー一覧取得ロジックを再設計
- 教師の複数割当（担任・副担任・学年主任・教科担当）に対応
- ログアウト処理の責務を Store に集約  
  （詳細：Backend / Frontend Changelog）

---

## 2026/02/04
- ログイン時に返却するユーザー情報設計を整理
- 生徒・教師で取得する学年／クラス情報の責務を明確化
- Journal API 操作用スクリプトを追加
- 開発環境で scripts ディレクトリを参照可能に改善  
  （詳細：Backend Changelog / Design Docs）

---

## 2026/02/03
- 連絡帳（Journal）機能の画面実装を追加
- 開発環境のデータ投入方針を整理  
  （詳細：Frontend / Backend Changelog）

---

## 2026/02/01
- 認証初期化フロー（initAuth）の設計を改善
- 管理者向けユーザー一覧取得処理の内部構造を整理  
  （詳細：Backend Changelog）

---

## 2026/01/26
- 認証方式を interceptor 中心の構成へ変更
- 設計ドキュメントの分割・整理を実施  
  （詳細：Design Docs）

---

## 2026/01/23
- ログイン後の共通ヘッダー／フッターを実装
- 教師担当情報管理ロジックを改善  
  （詳細：Frontend / Backend Changelog）

---

## 2026/01/16
- トークン管理方式をアクセストークン／リフレッシュトークン構成へ変更  
  （詳細：Design Docs）

---

## 2025/12/30
- 認証・ルーティング・状態管理の基盤実装を完了
- フロントエンド／バックエンド連携を確立

---

## 2025/12/20
- 連絡帳システムを新規プロジェクトとして再構築
- FastAPI + Vue + Docker を用いた初期構成を作成
