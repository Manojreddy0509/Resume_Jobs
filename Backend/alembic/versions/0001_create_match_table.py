"""create matches table

Revision ID: 0002_create_matches_table
Revises: 
Create Date: 2025-12-25 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0002_create_matches_table"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "matches",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("resume_id", sa.String(), sa.ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("job_id", sa.String(), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("breakdown", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    # optional index on (job_id, score) for ranking queries
    op.create_index("ix_matches_job_score", "matches", ["job_id", "score"])

def downgrade():
    op.drop_index("ix_matches_job_score", table_name="matches")
    op.drop_table("matches")
