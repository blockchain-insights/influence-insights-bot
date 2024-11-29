"""Anomaly changed to classification

Revision ID: 002
Revises: 001
Create Date: 2024-11-29 17:23:27.649399

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the column from anomaly_type to classification_type
    op.alter_column('tweets', 'anomaly_type', new_column_name='classification_type')


def downgrade() -> None:
    # Rename the column back from classification_type to anomaly_type
    op.alter_column('tweets', 'classification_type', new_column_name='anomaly_type')
