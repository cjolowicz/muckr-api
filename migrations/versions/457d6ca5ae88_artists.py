"""artists

Revision ID: 457d6ca5ae88
Revises: 38a6b4811501
Create Date: 2018-12-23 13:53:45.477425
"""

from alembic import op
import sqlalchemy as sa


revision = '457d6ca5ae88'
down_revision = '38a6b4811501'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'artists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index(
        op.f('ix_artists_name'),
        'artists',
        ['name'],
        unique=False,
    )


def downgrade():
    op.drop_index(
        op.f('ix_artists_name'),
        table_name='artists',
    )

    op.drop_table('artists')
