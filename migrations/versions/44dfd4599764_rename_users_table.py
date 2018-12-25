"""Rename users table.

Revision ID: 44dfd4599764
Revises: 14e67e8e4248
Create Date: 2018-10-18 15:09:23.624967
"""

from alembic import op
import sqlalchemy as sa


revision = '44dfd4599764'
down_revision = '14e67e8e4248'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('password_hash', sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(
        op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')


def downgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('username', sa.VARCHAR(length=64), nullable=True),
        sa.Column('email', sa.VARCHAR(length=120), nullable=True),
        sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=1)
    op.create_index('ix_user_email', 'user', ['email'], unique=1)
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
