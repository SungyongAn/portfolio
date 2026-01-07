"""merge multiple heads

Revision ID: ac794473c081
Revises: aaaa_recreate_admin_user_argon2, c2e69214c9ec
Create Date: 2026-01-07 13:45:35.268999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac794473c081'
down_revision: Union[str, Sequence[str], None] = ('aaaa_recreate_admin_user_argon2', 'c2e69214c9ec')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
