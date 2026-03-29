"""add indexes

Revision ID: 004
Revises: 003
Create Date: 2026-03-27

"""

import sqlalchemy as sa

from alembic import op

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade():
    # 1. NULL許容でカラム追加
    op.add_column(
        "measurements",
        sa.Column("manager_confirmed", sa.Boolean(), nullable=True),
    )

    # 2. 既存データ更新（条件付き）
    # status = 'approved' の場合 TRUE
    op.execute(
        """
        UPDATE measurements
        SET manager_confirmed = TRUE
        WHERE status = 'approved'
        """
    )

    # それ以外は FALSE
    op.execute(
        """
        UPDATE measurements
        SET manager_confirmed = FALSE
        WHERE manager_confirmed IS NULL
        """
    )

    # 3. NOT NULL制約 + デフォルト付与
    op.alter_column(
        "measurements",
        "manager_confirmed",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.false(),
    )


def downgrade():
    op.drop_column("measurements", "manager_confirmed")
