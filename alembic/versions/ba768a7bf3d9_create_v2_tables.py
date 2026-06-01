"""create v2 tables

Revision ID: ba768a7bf3d9
Revises: 3854d17fe61d
Create Date: 2026-05-06 08:42:30.878087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision = "ba768a7bf3d9"
down_revision = "3854d17fe61d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "restaurants",
        sa.Column("restaurant_id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("location", sa.Text(), nullable=False),
        sa.Column("cuisine", sa.Text(), nullable=False),
        sa.Column("price_range", sa.Integer(), nullable=False),
        sa.Column("allergen_free_options", sa.Boolean(), nullable=False),
        sa.Column("allows_animals", sa.Boolean(), nullable=False),
    )

    op.create_table(
        "saved_restaurants",
        sa.Column("saved_restaurant_id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Text(), nullable=False),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.Column(
            "saved_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    op.create_table(
        "owner_replies",
        sa.Column("reply_id", sa.Integer(), primary_key=True),
        sa.Column("review_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Text(), nullable=False),
        sa.Column("reply", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    op.create_table(
        "review_reports",
        sa.Column("report_id", sa.Integer(), primary_key=True),
        sa.Column("review_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("review_reports")
    op.drop_table("owner_replies")
    op.drop_table("saved_restaurants")
    op.drop_table("restaurants")
