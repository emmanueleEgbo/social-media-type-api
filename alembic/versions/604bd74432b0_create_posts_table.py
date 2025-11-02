"""create posts table

Revision ID: 604bd74432b0
Revises: 
Create Date: 2025-10-31 23:18:58.721526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '604bd74432b0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
