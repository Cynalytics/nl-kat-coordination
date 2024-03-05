"""Add schedules table

Revision ID: 0008
Revises: 0007
Create Date: 2024-01-30 15:08:44.084080

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

import scheduler

# revision identifiers, used by Alembic.
revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "schedules",
        sa.Column("id", scheduler.utils.datastore.GUID(), nullable=False),
        sa.Column("scheduler_id", sa.String(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("p_item", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("cron_expression", sa.String(), nullable=True),
        sa.Column("deadline_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("modified_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_runs",
        sa.Column("id", scheduler.utils.datastore.GUID(), nullable=False),
        sa.Column("scheduler_id", sa.String(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("p_item", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("schedule_id", scheduler.utils.datastore.GUID(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING", "QUEUED", "DISPATCHED", "RUNNING", "COMPLETED", "FAILED", "CANCELLED", name="taskstatus"
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("modified_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["schedule_id"], ["schedules.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_p_item_hash", "task_runs", [sa.text("(p_item->>'hash')"), sa.text("created_at DESC")], unique=False
    )
    op.drop_index("ix_tasks_p_item_hash", table_name="tasks")
    op.drop_table("tasks")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("scheduler_id", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM(
                "PENDING", "QUEUED", "DISPATCHED", "RUNNING", "COMPLETED", "FAILED", "CANCELLED", name="taskstatus"
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "modified_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("p_item", postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=False),
        sa.Column("type", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="tasks_pkey"),
    )
    op.create_index(
        "ix_tasks_p_item_hash",
        "tasks",
        [sa.text("(p_item ->> 'hash'::text)"), sa.text("created_at DESC")],
        unique=False,
    )
    op.drop_index("ix_p_item_hash", table_name="task_runs")
    op.drop_table("task_runs")
    op.drop_table("schedules")
    # ### end Alembic commands ###