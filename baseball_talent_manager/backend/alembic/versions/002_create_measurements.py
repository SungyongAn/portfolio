"""create measurements table

Revision ID: 002
Revises: 001
Create Date: 2026-03-01

"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'measurements',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('measurement_date', sa.Date(), nullable=False),
        sa.Column('sprint_50m', sa.Float(), nullable=False),
        sa.Column('base_running', sa.Float(), nullable=False),
        sa.Column('throwing_distance', sa.Float(), nullable=False),
        sa.Column('pitch_speed', sa.Float(), nullable=False),
        sa.Column('batting_speed', sa.Float(), nullable=False),
        sa.Column('swing_speed', sa.Float(), nullable=False),
        sa.Column('bench_press', sa.Float(), nullable=False),
        sa.Column('squat', sa.Float(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )


def downgrade():
    op.drop_table('measurements')