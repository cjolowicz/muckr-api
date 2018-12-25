"""user.is_admin

Revision ID: 38a6b4811501
Revises: 91cf97f543f6
Create Date: 2018-10-19 18:51:28.728578
"""

from alembic import op
import sqlalchemy as sa


revision = '38a6b4811501'
down_revision = '91cf97f543f6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column('is_admin', sa.Boolean(), nullable=True),
    )


def downgrade():
    op.drop_column(
        'users',
        'is_admin',
    )
