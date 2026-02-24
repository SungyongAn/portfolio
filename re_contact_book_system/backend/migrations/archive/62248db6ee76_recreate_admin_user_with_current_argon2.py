from alembic import op
from sqlalchemy.sql import text

revision = "aaaa_recreate_admin_user_argon2"
down_revision = "zzzz_recreate_admin_user"
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
                '$argon2id$v=19$m=65536,t=3,p=4$n/P+P+d8r/V+7907x/j/fw$a8baIAcJW/o+HX5nCpoC9GjN5L1MeTDsDeXrKz+ZeYo',
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
