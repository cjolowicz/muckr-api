"""tokens

Revision ID: 91cf97f543f6
Revises: 44dfd4599764
Create Date: 2018-10-19 18:23:59.423989
"""

from alembic import op
import sqlalchemy as sa


revision = '91cf97f543f6'
down_revision = '44dfd4599764'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
                  sa.Column('token', sa.String(length=64), nullable=True))
    op.add_column('users',
                  sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_users_token'), 'users', ['token'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_users_token'), table_name='users')
    op.drop_column('users', 'token_expiration')
    op.drop_column('users', 'token')
