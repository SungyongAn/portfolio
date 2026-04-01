"""add indexes

Revision ID: 003
Revises: 002
Create Date: 2026-03-27

"""

from alembic import op

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade():
    # usersテーブルへのインデックス追加
    op.create_index("ix_users_role", "users", ["role"])
    op.create_index("ix_users_status", "users", ["status"])

    # measurementsテーブルへのインデックス追加
    op.create_index("ix_measurements_status", "measurements", ["status"])
    op.create_index(
        "ix_measurements_measurement_date", "measurements", ["measurement_date"]
    )
    op.create_index(
        "ix_measurements_user_id_measurement_date",
        "measurements",
        ["user_id", "measurement_date"],
    )


def downgrade():
    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_status", table_name="users")
    op.drop_index("ix_measurements_status", table_name="measurements")
    op.drop_index("ix_measurements_measurement_date", table_name="measurements")
    op.drop_index("ix_measurements_user_id_measurement_date", table_name="measurements")
