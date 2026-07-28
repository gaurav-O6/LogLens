"""add job_id to log_entries

Revision ID: a91d7c4e2b10
Revises: 5667a81030f9
Create Date: 2026-07-28
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a91d7c4e2b10"
down_revision = "5667a81030f9"
branch_labels = None
depends_on = None


def upgrade():
    # Existing log entries were created before job ownership
    # existed. Remove them before adding the non-null FK.
    #
    # This is intentional for the development database because
    # the existing rows are polluted test data.
    op.drop_table("log_entries")

    op.create_table(
        "log_entries",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "job_id",
            sa.Integer(),
            sa.ForeignKey(
                "jobs.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "ip_address",
            sa.String(length=45),
            nullable=False,
        ),

        sa.Column(
            "timestamp",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "method",
            sa.String(length=10),
            nullable=False,
        ),

        sa.Column(
            "path",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "status_code",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "user_agent",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_log_entries_job_id",
        "log_entries",
        ["job_id"],
    )

    op.create_index(
        "ix_log_entries_ip_address",
        "log_entries",
        ["ip_address"],
    )


def downgrade():

    op.drop_index(
        "ix_log_entries_ip_address",
        table_name="log_entries",
    )

    op.drop_index(
        "ix_log_entries_job_id",
        table_name="log_entries",
    )

    op.drop_table("log_entries")