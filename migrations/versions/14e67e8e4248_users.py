"""users"""

from alembic import op
import sqlalchemy as sa


revision = '14e67e8e4248'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('password_hash', sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index(
        op.f('ix_user_email'),
        'user',
        ['email'],
        unique=True,
    )

    op.create_index(
        op.f('ix_user_username'),
        'user',
        ['username'],
        unique=True,
    )


def downgrade():
    op.drop_index(
        op.f('ix_user_username'),
        table_name='user',
    )

    op.drop_index(
        op.f('ix_user_email'),
        table_name='user',
    )

    op.drop_table('user')
