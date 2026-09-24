"""Initial schema migration

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-09-24 11:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("source", sa.String(length=64), nullable=False, index=True),
        sa.Column("source_profile_id", sa.String(length=128), nullable=False, index=True),
        sa.Column("candidate_code", sa.String(length=64), nullable=True),
        sa.Column("profile_url", sa.String(length=512), nullable=True),
        sa.Column("gender", sa.String(length=16), nullable=False, default="male", index=True),
        sa.Column("age", sa.Integer(), nullable=True, index=True),
        sa.Column("height_cm", sa.Float(), nullable=True, index=True),
        sa.Column("height_display", sa.String(length=32), nullable=True),
        sa.Column("marital_status", sa.String(length=64), nullable=False, default="never_married", index=True),
        sa.Column("current_location", sa.String(length=128), nullable=True, index=True),
        sa.Column("permanent_location", sa.String(length=128), nullable=True, index=True),
        sa.Column("education", sa.JSON(), nullable=False),
        sa.Column("career", sa.JSON(), nullable=False),
        sa.Column("deen", sa.JSON(), nullable=False),
        sa.Column("synthetic", sa.Boolean(), nullable=False, default=False),
        sa.Column("raw_data", sa.JSON(), nullable=True),
        sa.Column("first_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_updated", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "profile_versions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("profile_id", sa.String(length=64), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("change_type", sa.String(length=64), nullable=False),
        sa.Column("field_name", sa.String(length=64), nullable=False),
        sa.Column("old_value", sa.Text(), nullable=True),
        sa.Column("new_value", sa.Text(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "search_profiles",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, default=False),
        sa.Column("criteria", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "shortlists",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("profile_id", sa.String(length=64), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("stage", sa.String(length=64), nullable=False, default="Shortlisted"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "notes",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("profile_id", sa.String(length=64), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "sources",
        sa.Column("name", sa.String(length=64), primary_key=True),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, default=False),
        sa.Column("mode", sa.String(length=64), nullable=False, default="disabled"),
        sa.Column("terms_compliance_notes", sa.Text(), nullable=True),
        sa.Column("permits_automated_collection", sa.Boolean(), nullable=False, default=False),
        sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("sources")
    op.drop_table("notes")
    op.drop_table("shortlists")
    op.drop_table("search_profiles")
    op.drop_table("profile_versions")
    op.drop_table("profiles")
