"""Initial migration

Revision ID: 785c4258f09f
Revises: 3e21c478e88e
Create Date: 2024-12-12 22:53:18.073992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP

# revision identifiers, used by Alembic.
revision: str = '785c4258f09f'
down_revision: Union[str, None] = '3e21c478e88e'
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
