# 教師担当設計書（Teacher Assignment Design）

本ドキュメントは、教師の担当情報（担任・教科・学年主任等）の
データ設計およびバリテーション設計方針を整理するものである。

本設計は CHANGELOG（2026/01/20〜01/22）の設計変更を統合した結果である。

---

## 1. 背景

当初設計では、教師の教科情報を文字列で保持していたが、
以下の課題があった。

- 表記揺れが発生する
- 拡張（有効/無効管理）が困難
- 検索・集計が複雑

---

## 2. 設計方針

- 教師の担当情報は **正規化されたマスタ構造**で管理する
- 担当種別（assignment_type）によって **必須項目を変える**
- DB 制約ではなく **Service 層で意味的整合性を担保**する

---

## 3. テーブル構成

### 3.1 subjects（教科マスタ）

- name：教科名（UNIQUE）
- is_active：有効/無効管理

### 3.2 teacher_assignments

| カラム | 説明 |
|---|---|
| teacher_id | 教師ID |
| assignment_type | 担当種別 |
| grade_id | 学年 |
| class_id | クラス |
| subject_id | 教科 |

---

## 4. assignment_type 別設計

### 4.1 homeroom（担任）

- grade_id：必須
- class_id：必須
- subject_id：NULL
- is_primary：1 クラスにつき 1 人のみ

### 4.2 subject（教科担当）

- grade_id：必須
- class_id：必須
- subject_id：必須

### 4.3 grade_head（学年主任）

- grade_id：必須
- class_id：NULL
- subject_id：NULL

### 4.4 administrator（管理的役割）

- grade_id / class_id / subject_id：すべて NULL

---

## 5. バリテーション設計

- assignment_type ごとの必須項目チェックは
  **Service 層で明示的に制御**
- DB は外部キー整合性のみを保証する

※ 詳細は `validation.md` を参照

---

## 6. CHANGELOG との対応関係

| 日付 | 内容 |
|---|---|
| 2026/01/20 | 表示ロジック改善 |
| 2026/01/22 | subjects テーブル追加 |
| 2026/01/22 | 文字列管理廃止 |

---
