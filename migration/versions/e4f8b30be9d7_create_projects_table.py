"""Create projects table

Revision ID: e4f8b30be9d7
Revises: 785c4258f09f
Create Date: 2024-12-12 23:02:57.459203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP

# revision identifiers, used by Alembic.
revision: str = 'e4f8b30be9d7'
down_revision: Union[str, None] = '785c4258f09f'
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
