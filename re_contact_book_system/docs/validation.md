## 本ドキュメントの位置づけ

本ドキュメントは、本システムにおける
- 業務バリテーション設計の基準
- Service 層実装時の判断根拠
- 各設計ドキュメント（auth / assignment 等）から参照される共通ルール

を兼ねる。

# バリテーション設計書

本ドキュメントは、本システムにおける **業務バリテーション（アプリケーションレベルの制約）** を定義するものである。

本プロジェクトでは、DB（ER図・マイグレーション）は **構造の整合性** のみを担保し、
「誰が・何を・どの条件で操作できるか」という **意味的制約** はバックエンド（Service 層）で管理する。

---

## 1. バリテーションの基本方針

### 1.1 レイヤー構成

バリテーションは以下の 3 層構造で設計する。

1. **共通バリテーション**（全ロール共通）
2. **ロール別バリテーション**（student / teacher）
3. **業務バリテーション**（assignment_type 等）

※ 管理者（admin）は業務主体ではないため、共通バリテーション内で例外的に扱う。

---

## 2. 共通バリテーション

### 2.1 ユーザー・権限

* 操作対象の user_id は必ず存在すること
* users.role は以下のいずれかであること

  * `student`
  * `teacher`
  * `admin`

### 2.2 外部キー整合性

* grade_id / class_id / student_id / teacher_id は、対応するテーブルに存在すること
* Enum カラムは定義済みの値のみを許可する

### 2.3 管理者（admin）の扱い

管理者は以下の制約を **例外的に回避可能** とする。

* role による操作制限
* teacher_assignments の代理作成・更新
* 他ユーザー情報の管理操作

---

## 3. 生徒（student）のバリテーション

### 3.1 対象テーブル

* users
* student_class_assignments
* journal_entries
* teacher_notes（閲覧のみ）

---

### 3.2 student_class_assignments（クラス割当）

**ルール**

* student_id の role は `student` であること
* class_id は必須
* is_current = true のレコードは **1 生徒につき 1 件のみ**

**制限**

* 生徒自身による作成・更新は禁止

---

### 3.3 journal_entries（連絡帳）

**作成**

* student_id はログインユーザー自身
* entry_date / submission_date は必須
* physical_condition / mental_condition は必須

**参照・更新**

* 生徒は自分自身の連絡帳のみ参照可能
* is_read / read_by / read_at の更新は禁止

---

### 3.4 teacher_notes（教師メモ）

* 作成・更新：不可
* 閲覧：is_shared = true のみ可能

---

## 4. 教師（teacher）のバリテーション

### 4.1 対象テーブル

* teacher_assignments
* journal_entries（閲覧・既読）
* teacher_notes

---

### 4.2 teacher_assignments（教師割当）

#### 共通ルール

* teacher_id の role は `teacher`
* assignment_type は Enum 定義値のみ

#### assignment_type 別ルール

##### homeroom（担任）

* grade_id：必須
* class_id：必須
* subject_id：NULL
* is_primary = true は 1 クラスにつき 1 人のみ

##### subject（教科担当）

* grade_id：必須
* class_id：必須
* subject_id：必須

##### grade_head（学年主任）

* grade_id：必須
* class_id：NULL
* subject_id：NULL

##### administrator（管理的役割）

* grade_id：NULL
* class_id：NULL
* subject_id：NULL

---

### 4.3 journal_entries（連絡帳）

* 作成：不可
* 閲覧：担当クラスの生徒のみ
* 既読処理：可

---

### 4.4 teacher_notes（教師メモ）

* 作成：可
* 更新：自分が作成したメモのみ
* 閲覧：同学年共有（is_shared = true）

---

## 5. 補足

* 本ドキュメントは DB マイグレーション（ER 図）を根拠に作成している
* 将来テーブル分割・正規化を行う場合は、本バリテーションを先に見直すこと

---

## 改訂履歴

* 初版作成
