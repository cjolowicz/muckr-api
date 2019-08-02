"""Create table venues."""

from alembic import op
import sqlalchemy as sa


revision = "17b2d9bb4a15"
down_revision = "a84bc26c065d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "venues",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("city", sa.String(length=128), nullable=True),
        sa.Column("country", sa.String(length=128), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_venues_name"), "venues", ["name"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_venues_name"), table_name="venues")
    op.drop_table("venues")
