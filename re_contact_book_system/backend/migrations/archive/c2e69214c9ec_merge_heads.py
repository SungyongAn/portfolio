"""merge heads

Revision ID: c2e69214c9ec
Revises: zzzz_fix_admin_password, zzzz_recreate_admin_user
Create Date: 2026-01-07 11:24:38.399274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2e69214c9ec'
down_revision: Union[str, Sequence[str], None] = ('zzzz_fix_admin_password', 'zzzz_recreate_admin_user')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
