"""add content column to posts table

Revision ID: e1b2dfff8992
Revises: 604bd74432b0
Create Date: 2025-11-01 00:46:11.777345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1b2dfff8992'
down_revision: Union[str, Sequence[str], None] = '604bd74432b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
