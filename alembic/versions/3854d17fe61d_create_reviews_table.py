"""create reviews table

Revision ID: 3854d17fe61d
Revises: 
Create Date: 2026-05-04 13:42:13.174970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3854d17fe61d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'reviews',
        sa.Column('review_id', sa.Integer, primary_key=True),
        sa.Column('rating', sa.Float, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('food_quality_score', sa.Float, nullable=True),
        sa.Column('service_score', sa.Float, nullable=True),
        sa.Column('romantic_score', sa.Float, nullable=True),
        sa.Column('pricing_score', sa.Float, nullable=True),
        sa.Column('photos', sa.String, nullable=True),
        sa.Column(
            'created_at',
            sa.TIMESTAMP,
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.Column(
            'updated_at',
            sa.TIMESTAMP,
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
    )


def downgrade():
    op.drop_table('reviews')
