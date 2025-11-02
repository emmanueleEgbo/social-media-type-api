"""add users table

Revision ID: 9a7627fbdf3b
Revises: e1b2dfff8992
Create Date: 2025-11-01 00:55:32.551588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a7627fbdf3b'
down_revision: Union[str, Sequence[str], None] = 'e1b2dfff8992'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
      
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
