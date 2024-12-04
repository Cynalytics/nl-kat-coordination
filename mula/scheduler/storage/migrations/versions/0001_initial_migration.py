"""Initial migration
Revision ID: 0001
Revises:
Create Date: 2022-07-25 11:02:13.395259
"""

import sqlalchemy as sa
from alembic import op

import scheduler

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # First version of the scheduler didn't use alembic, so we have to check
    # whether the table exists before trying to create it
    bind = op.get_context().bind
    insp = sa.inspect(bind)
    if not insp.has_table("tasks"):
        # ### commands auto generated by Alembic - please adjust! ###
        op.create_table(
            "tasks",
            sa.Column("id", scheduler.utils.datastore.GUID(), nullable=False),
            sa.Column("hash", sa.String(), nullable=True),
            sa.Column("scheduler_id", sa.String(), nullable=True),
            sa.Column("task", sa.JSON(), nullable=False),
            sa.Column(
                "status",
                sa.Enum("PENDING", "QUEUED", "DISPATCHED", "RUNNING", "COMPLETED", "FAILED", name="taskstatus"),
                nullable=False,
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("modified_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tasks")
    # ### end Alembic commands ###