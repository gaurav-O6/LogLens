"""add is_private_ip column

Revision ID: b6a6cc95e19e
Revises: 71f02225f443
Create Date: 2026-07-23
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b6a6cc95e19e"
down_revision = "71f02225f443"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("detections") as batch_op:
        batch_op.add_column(
            sa.Column(
                "is_private_ip",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )


def downgrade():
    with op.batch_alter_table("detections") as batch_op:
        batch_op.drop_column("is_private_ip")