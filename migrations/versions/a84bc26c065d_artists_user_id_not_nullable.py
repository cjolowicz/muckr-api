"""artists.user_id not nullable

Revision ID: a84bc26c065d
Revises: 97089ffc8c1f
Create Date: 2018-12-25 11:14:06.151643
"""

import alembic.op
import sqlalchemy as sa


revision = 'a84bc26c065d'
down_revision = '97089ffc8c1f'
branch_labels = None
depends_on = None


def upgrade():
    alembic.op.alter_column(
        'artists',
        'user_id',
        existing_type=sa.INTEGER(),
        nullable=False,
    )


def downgrade():
    alembic.op.alter_column(
        'artists',
        'user_id',
        existing_type=sa.INTEGER(),
        nullable=True,
    )
