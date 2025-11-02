"""add foreign key to post table

Revision ID: 501a9179c2e1
Revises: 9a7627fbdf3b
Create Date: 2025-11-02 21:08:31.788868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '501a9179c2e1'
down_revision: Union[str, Sequence[str], None] = '9a7627fbdf3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_user_fk', table_name="posts")
    op.drop_column('posts', 'ower_id')