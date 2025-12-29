"""add pgvector extension, add vector columns, migrate JSONB embeddings to vector, and add index

Revision ID: 0003_add_pgvector_and_columns
Revises: d8f13af35751
Create Date: 2025-12-26 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# NOTE: set DIM to your embedding size (OpenAI text-embedding-3-small => 1536)
DIM = 1536

revision = "0003_add_pgvector_and_columns"
down_revision = "d8f13af35751"
branch_labels = None
depends_on = None


def upgrade():
    # 1) enable extension (if not present)
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2) add new vector columns for resumes and jobs
    op.add_column("resumes", sa.Column("embedding_vector", postgresql.ARRAY(sa.Float()), nullable=True))
    op.add_column("jobs", sa.Column("embedding_vector", postgresql.ARRAY(sa.Float()), nullable=True))

    # 3) migrate JSONB embeddings -> embedding_vector safely (only when dims match)
    # We will use a SQL statement that casts jsonb array to float[] then to vector conceptually.
    # Since direct vector type isn't available via SQLAlchemy here, we store float[] and later alter to vector via raw SQL.
    #
    # Populate embedding_vector FROM JSONB embedding where length matches DIM
    op.execute(
        sa.text(
            f"""
            UPDATE resumes
            SET embedding_vector = (
                SELECT array_agg((e)::double precision)
                FROM jsonb_array_elements_text(embedding) AS e
            )
            WHERE embedding IS NOT NULL AND jsonb_array_length(embedding) = :dim
            """
        ),
        {"dim": DIM},
    )

    op.execute(
        sa.text(
            f"""
            UPDATE jobs
            SET embedding_vector = (
                SELECT array_agg((e)::double precision)
                FROM jsonb_array_elements_text(embedding) AS e
            )
            WHERE embedding IS NOT NULL AND jsonb_array_length(embedding) = :dim
            """
        ),
        {"dim": DIM},
    )

    # 4) alter column types from float[] -> vector(DIM)
    # Use raw SQL to ALTER type: cast float[] to vector by using '::vector'
    op.execute(f"ALTER TABLE resumes ALTER COLUMN embedding_vector TYPE vector({DIM}) USING embedding_vector::vector;")
    op.execute(f"ALTER TABLE jobs ALTER COLUMN embedding_vector TYPE vector({DIM}) USING embedding_vector::vector;")

    # 5) create ivfflat index for cosine distance (choose lists based on data; 100 is a sensible start)
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_resumes_embedding_ivfflat ON resumes USING ivfflat (embedding_vector vector_cosine_ops) WITH (lists = 100);"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_jobs_embedding_ivfflat ON jobs USING ivfflat (embedding_vector vector_cosine_ops) WITH (lists = 100);"
    )


def downgrade():
    # drop indices and columns, drop extension (keep caution)
    op.execute("DROP INDEX IF EXISTS idx_resumes_embedding_ivfflat;")
    op.execute("DROP INDEX IF EXISTS idx_jobs_embedding_ivfflat;")

    # cast back to float[]: use USING embedding_vector::float8[] if needed, but we'll drop columns to be safe
    op.drop_column("resumes", "embedding_vector")
    op.drop_column("jobs", "embedding_vector")

    # DO NOT drop extension automatically in downgrade in prod — leaving it out is safer.
    # op.execute("DROP EXTENSION IF EXISTS vector;")
