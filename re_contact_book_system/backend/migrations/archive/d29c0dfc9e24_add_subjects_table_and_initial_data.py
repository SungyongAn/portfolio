"""add subjects table and initial data

Revision ID: d29c0dfc9e24
Revises: 909b55b0e5b4
Create Date: 2026-01-26 06:44:42.610245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd29c0dfc9e24'
down_revision: Union[str, Sequence[str], None] = '909b55b0e5b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # subjects テーブルはすでに存在している前提
    # 初期教科データの挿入（重複は無視）
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
    # 今回は初期データの削除のみ
    op.execute("""
    DELETE FROM subjects
    WHERE name IN (
        '国語','社会','数学','理科','音楽','美術','保健体育','技術・家庭','英語'
    );
    """)