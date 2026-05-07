"""add role column to users

Revision ID: f27ae7331ca7
Revises: 
Create Date: 2026-05-04 08:37:41.772420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f27ae7331ca7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("users", "role")
