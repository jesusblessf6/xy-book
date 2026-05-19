"""make_root_post_id_nullable

Revision ID: 57f709bce3e9
Revises: 3d6e61f147d0
Create Date: 2026-05-19 12:44:56.220782
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '57f709bce3e9'
down_revision: Union[str, None] = '3d6e61f147d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('posts', 'root_post_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('posts', 'thread_path',
               existing_type=sa.String(500),
               nullable=False,
               server_default='')


def downgrade() -> None:
    op.alter_column('posts', 'root_post_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('posts', 'thread_path',
               existing_type=sa.String(500),
               nullable=False,
               server_default=None)
