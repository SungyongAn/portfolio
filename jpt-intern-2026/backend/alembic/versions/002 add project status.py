"""add project status IN_PROGRESS COMPLETED DRAFT

Revision ID: 002_add_project_status
Revises: 001_create_initial_tables
Create Date: 2026-04-21

"""

from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # MySQLのENUM型に新しい値を追加する
    op.execute(
        "ALTER TABLE projects MODIFY COLUMN status "
        "ENUM('DRAFT','PENDING_DEPT','PENDING_HQ','APPROVED','IN_PROGRESS','COMPLETED','REJECTED') "
        "NOT NULL"
    )


def downgrade() -> None:
    # 既存データに IN_PROGRESS / COMPLETED / DRAFT が含まれていない前提で戻す
    op.execute(
        "ALTER TABLE projects MODIFY COLUMN status "
        "ENUM('PENDING_DEPT','PENDING_HQ','APPROVED','REJECTED') "
        "NOT NULL"
    )
