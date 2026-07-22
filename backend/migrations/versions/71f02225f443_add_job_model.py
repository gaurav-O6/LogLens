"""add job model

Revision ID: 71f02225f443
Revises: f00814b65a1a
Create Date: 2026-07-19 01:49:17.037088

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71f02225f443'
down_revision = 'f00814b65a1a'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_jobs_status'),
            ['status'],
            unique=False
        )


def downgrade():

    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.drop_index(
            batch_op.f('ix_jobs_status')
        )


    op.drop_table('jobs')