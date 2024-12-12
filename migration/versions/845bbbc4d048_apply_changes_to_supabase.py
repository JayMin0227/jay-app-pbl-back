"""Apply changes to Supabase

Revision ID: 845bbbc4d048
Revises: 657281998164
Create Date: 2024-12-12 18:27:18.193860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP

# revision identifiers, used by Alembic.
revision: str = '845bbbc4d048'
down_revision: Union[str, None] = '657281998164'
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
