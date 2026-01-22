"""add subjects table and refactor teacher_assignments

Revision ID: 909b55b0e5b4
Revises: ac794473c081
Create Date: 2026-01-22 02:29:18.342767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '909b55b0e5b4'
down_revision: Union[str, Sequence[str], None] = 'ac794473c081'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ① subjects テーブル作成
    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.true()),
        sa.UniqueConstraint("name", name="uk_subject_name"),
    )

    # ② subject_name を削除
    op.drop_column("teacher_assignments", "subject_name")

    # ③ subject_id を追加
    op.add_column(
        "teacher_assignments",
        sa.Column(
            "subject_id",
            sa.Integer,
            sa.ForeignKey("subjects.id", ondelete="CASCADE"),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("teacher_assignments", "subject_id")

    op.add_column(
        "teacher_assignments",
        sa.Column("subject_name", sa.String(50)),
    )

    op.drop_table("subjects")