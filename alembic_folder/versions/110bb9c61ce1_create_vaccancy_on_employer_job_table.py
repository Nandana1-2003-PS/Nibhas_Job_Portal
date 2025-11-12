"""create vaccancy on employer_job table

Revision ID: 110bb9c61ce1
Revises: 
Create Date: 2025-11-10 10:10:13.556445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '110bb9c61ce1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('employer_jobs',sa.Column('vacancy',sa.Integer(),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('employer_jobs','vacancy')
