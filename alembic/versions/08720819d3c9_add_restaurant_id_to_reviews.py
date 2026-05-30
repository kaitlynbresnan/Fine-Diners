"""add_restaurant_id_to_reviews

Revision ID: 08720819d3c9
Revises: ba768a7bf3d9
Create Date: 2026-05-11 12:48:15.727055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08720819d3c9'
down_revision: Union[str, None] = 'ba768a7bf3d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('reviews', sa.Column('restaurant_id', sa.Integer(), nullable=True))

    op.create_foreign_key(
        'fk_reviews_restaurant_id',
        'reviews',
        'restaurants',
        ['restaurant_id'],
        ['restaurant_id']
    )


def downgrade() -> None:
    op.drop_constraint('fk_reviews_restaurant_id', 'reviews', type='foreignkey')
    op.drop_column('reviews', 'restaurant_id')