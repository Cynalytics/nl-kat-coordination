"""Add cron field

Revision ID: 9f48560b0000
Revises: 870fc302b852
Create Date: 2024-09-18 13:12:40.926394

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9f48560b0000"
down_revision = "a2c8d54b0124"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("boefje", sa.Column("cron", sa.String(length=128), nullable=True))
    op.add_column("boefje", sa.Column("interval", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("boefje", "interval")
    op.drop_column("boefje", "cron")
    # ### end Alembic commands ###
