"""artists belong to users

Revision ID: 97089ffc8c1f
Revises: 457d6ca5ae88
Create Date: 2018-12-23 14:49:28.347766
"""

from alembic import op
import sqlalchemy as sa


revision = '97089ffc8c1f'
down_revision = '457d6ca5ae88'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'artists',
        sa.Column('user_id', sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        None,
        'artists',
        'users',
        ['user_id'],
        ['id'],
    )


def downgrade():
    op.drop_constraint(
        None,
        'artists',
        type_='foreignkey',
    )

    op.drop_column(
        'artists',
        'user_id',
    )
