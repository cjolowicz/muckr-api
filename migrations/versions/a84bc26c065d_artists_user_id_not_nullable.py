"""Make column artists.user_id NOT NULL."""

from alembic import op
import sqlalchemy as sa


revision = 'a84bc26c065d'
down_revision = '97089ffc8c1f'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('artists', 'user_id', existing_type=sa.INTEGER(), nullable=False)


def downgrade():
    op.alter_column('artists', 'user_id', existing_type=sa.INTEGER(), nullable=True)
