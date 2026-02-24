"""insert_admin_account

Revision ID: f8884f1ab218
Revises: 15cfb19c6a4c
Create Date: 2026-02-03 02:26:56.250783

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = 'f8884f1ab218'
down_revision: Union[str, Sequence[str], None] = '15cfb19c6a4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
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