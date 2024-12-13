"""Create projects table

Revision ID: fd0e06f3ac3f
Revises: e17b3239576f
Create Date: 2024-12-13 22:24:46.065301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fd0e06f3ac3f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.create_table(
        'ideas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('tags', sa.Text),
    )

def downgrade():
    op.drop_table('ideas')