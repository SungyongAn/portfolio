from alembic import op
from sqlalchemy.sql import text

revision = "zzzz_fix_admin_password"
down_revision = "yyyy_add_initial_admin_user"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        UPDATE users
        SET password_hash = '$2b$12$w1s4c8r1zG5jN8mH3cZl5e7Q5n5n6sYQk8ZCkY4nXz3rK8lFvK6iS'
        WHERE email = 'admin@school.ac.jp'
    """)


def downgrade():
    pass
