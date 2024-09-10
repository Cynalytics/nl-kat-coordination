"""Remove environment keys field

Revision ID: 870fc302b852
Revises: 5be152459a7b
Create Date: 2024-08-20 06:08:20.943924

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "870fc302b852"
down_revision = "5be152459a7b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("boefje", "environment_keys")
    op.drop_column("normalizer", "environment_keys")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "normalizer",
        sa.Column("environment_keys", postgresql.ARRAY(sa.VARCHAR(length=128)), autoincrement=False, nullable=False),
    )
    op.add_column(
        "boefje",
        sa.Column("environment_keys", postgresql.ARRAY(sa.VARCHAR(length=128)), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###