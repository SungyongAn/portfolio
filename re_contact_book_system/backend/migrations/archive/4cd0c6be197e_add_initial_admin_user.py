from alembic import op 
from sqlalchemy.sql import text 

revision = "yyyy_add_initial_admin_user" 
down_revision = "xxxx_initial_tables" 
branch_labels = None
depends_on = None 


def upgrade():
    op.execute(
        text(
            """ 
            INSERT INTO users
            (email, password_hash, role, name)
            SELECT
            'admin@school.ac.jp',
            '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oc2BdNpw5uze',
            'admin', 'システム管理者'
            WHERE NOT EXISTS 
            ( SELECT 1 FROM users WHERE email = 'admin@school.ac.jp' ) 
            """)
        )


def downgrade():
    op.execute(
        "DELETE FROM users WHERE email = 'admin@school.ac.jp'" 
        )
