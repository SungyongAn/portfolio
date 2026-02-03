from alembic import op
from sqlalchemy.sql import text

revision = "zzzz_recreate_admin_user"
down_revision = "yyyy_add_initial_admin_user"
branch_labels = None
depends_on = None


def upgrade():
    # ① 既存 admin を削除
    op.execute(
        text(
            """
            DELETE FROM users
            WHERE email = 'admin@school.ac.jp'
            """
        )
    )

    # ② 現在の構成で生成したハッシュで再作成
    op.execute(
        text(
            """
            INSERT INTO users (email, password_hash, role, name)
            VALUES (
                'admin@school.ac.jp',
                '$2b$12$ehzEI8IfJfuH5u6F2EoL9uHQG95H/d1CzFZVWWVo.Z3h9a7gWuNHi',
                'admin',
                'システム管理者'
            )
            """
        )
    )


def downgrade():
    # downgrade 時は admin を消すだけ
    op.execute(
        text(
            """
            DELETE FROM users
            WHERE email = 'admin@school.ac.jp'
            """
        )
    )
