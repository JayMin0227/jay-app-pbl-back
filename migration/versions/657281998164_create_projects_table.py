"""Create projects table

Revision ID: 657281998164
Revises: 
Create Date: 2024-12-12 18:00:33.418345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP

# revision identifiers, used by Alembic.
revision: str = '657281998164'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # テーブルを作成
    op.create_table(
        'ideas',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created_at', TIMESTAMP(timezone=True), nullable=False),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('tags', sa.Text, nullable=True),
    )


def downgrade() -> None:
    # テーブルを削除
    op.drop_table('ideas')
