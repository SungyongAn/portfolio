# users（ユーザー）

## カラム

| カラム名        | 型                                                          | NULL | デフォルト                  | 説明                         |
| --------------- | ----------------------------------------------------------- | ---- | --------------------------- | ---------------------------- |
| id              | INT                                                         | NO   | AUTO_INCREMENT              | ユーザーID                   |
| department_id   | INT                                                         | YES  | NULL                        | 部門ID                       |
| name            | VARCHAR(100)                                                | NO   | -                           | 氏名                         |
| email           | VARCHAR(255)                                                | NO   | -                           | メールアドレス（UNIQUE）     |
| hashed_password | VARCHAR(255)                                                | NO   | -                           | パスワードハッシュ（Argon2） |
| role            | ENUM('TASK_MEMBER','APPLICANT','DEPT_MANAGER','HQ_MANAGER') | NO   | -                           | ロール                       |
| created_at      | DATETIME                                                    | NO   | CURRENT_TIMESTAMP           | 作成日時                     |
| updated_at      | DATETIME                                                    | NO   | CURRENT_TIMESTAMP ON UPDATE | 更新日時                     |

## インデックス

```sql
PRIMARY KEY (id)
UNIQUE INDEX uq_users_email (email)
INDEX idx_users_department_id (department_id)
INDEX idx_users_role (role)
```

## 制約

```sql
FOREIGN KEY (department_id) REFERENCES departments(id)
```

## ロール定義

| 値           | 説明                                               |
| ------------ | -------------------------------------------------- |
| TASK_MEMBER  | 担当者（自部門案件のタスクを更新できる）           |
| APPLICANT    | 申請者（案件申請・タスク管理・予算実績入力を行う） |
| DEPT_MANAGER | 部門管理者（自部門案件の一次承認・進捗確認を行う） |
| HQ_MANAGER   | 本部管理者（全部門案件の最終承認・全体確認を行う） |

## 備考

- department_id について
  - ユーザーは原則として部門に所属する前提とするが、本部管理者など一部例外を考慮し NULL を許可している
- hashed_password について
  - Argon2 アルゴリズムでハッシュ化して保存する
