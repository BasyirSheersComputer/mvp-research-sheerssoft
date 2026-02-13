"""add_soft_delete

Revision ID: sd_001_add_soft_delete
Revises: enable_rls_001
Create Date: 2026-02-13 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'sd_001_add_soft_delete'
down_revision = 'enable_rls_001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('properties', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('conversations', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('messages', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('leads', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('leads', 'deleted_at')
    op.drop_column('messages', 'deleted_at')
    op.drop_column('conversations', 'deleted_at')
    op.drop_column('properties', 'deleted_at')
