"""insert_initial_subjects

Revision ID: 15cfb19c6a4c
Revises: 001_initial_schema
Create Date: 2026-02-03 02:23:10.378707

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '15cfb19c6a4c'
down_revision: Union[str, Sequence[str], None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # subjects テーブルは既存
    # 初期教科データを挿入（重複は無視）
    op.execute("""
    INSERT IGNORE INTO subjects (name, is_active) VALUES
        ('国語', TRUE),
        ('社会', TRUE),
        ('数学', TRUE),
        ('理科', TRUE),
        ('音楽', TRUE),
        ('美術', TRUE),
        ('保健体育', TRUE),
        ('技術・家庭', TRUE),
        ('英語', TRUE);
    """)


def downgrade():
    # 今回追加した初期教科データのみ削除
    op.execute("""
    DELETE FROM subjects
    WHERE name IN (
        '国語','社会','数学','理科','音楽','美術','保健体育','技術・家庭','英語'
    );
    """)